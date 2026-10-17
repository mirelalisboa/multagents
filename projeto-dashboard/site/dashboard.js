/* ES5 intencional: filtragem local, desenho SVG e tema sem bibliotecas ou rede. */
(function () {
  "use strict";

  var MONTHS = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];
  var LIGHT_CHART_COLORS = ["#542477", "#9257b2", "#b65c16", "#287660", "#315f9b"];
  var DARK_CHART_COLORS = ["#d8b4ff", "#ad7add", "#ffc477", "#7fd0b0", "#8ab8f0"];
  var rowsAll = [];

  function byId(id) {
    return document.getElementById(id);
  }

  function setText(node, text) {
    while (node.firstChild) {
      node.removeChild(node.firstChild);
    }
    node.appendChild(document.createTextNode(String(text)));
  }

  function formatInteger(value) {
    return String(Math.round(Number(value))).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  }

  function formatMoney(value) {
    var parts = Number(value).toFixed(2).split(".");
    return "R$\u00a0" + parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".") + "," + parts[1];
  }

  function svgNode(name, attributes, text) {
    var node = document.createElementNS("http://www.w3.org/2000/svg", name);
    var key;
    for (key in attributes) {
      if (Object.prototype.hasOwnProperty.call(attributes, key)) {
        node.setAttribute(key, String(attributes[key]));
      }
    }
    if (typeof text !== "undefined" && text !== "") {
      node.appendChild(document.createTextNode(String(text)));
    }
    return node;
  }

  function clearNode(node) {
    while (node.firstChild) {
      node.removeChild(node.firstChild);
    }
  }

  function makeSvg(container, title, titleId, viewBox) {
    var svg = svgNode("svg", {
      viewBox: viewBox,
      role: "img",
      "aria-labelledby": titleId,
      focusable: "false"
    });
    svg.appendChild(svgNode("title", { id: titleId }, title));
    clearNode(container);
    container.appendChild(svg);
    return svg;
  }

  function currentChartColors() {
    return document.body.className.indexOf("tema-escuro") !== -1 ? DARK_CHART_COLORS : LIGHT_CHART_COLORS;
  }

  function polar(cx, cy, radius, angle) {
    return { x: cx + radius * Math.cos(angle), y: cy + radius * Math.sin(angle) };
  }

  function fullDonutPath(cx, cy, outerRadius, innerRadius) {
    return "M " + cx + " " + (cy - outerRadius) +
      " A " + outerRadius + " " + outerRadius + " 0 1 1 " + cx + " " + (cy + outerRadius) +
      " A " + outerRadius + " " + outerRadius + " 0 1 1 " + cx + " " + (cy - outerRadius) + " Z " +
      "M " + cx + " " + (cy - innerRadius) +
      " A " + innerRadius + " " + innerRadius + " 0 1 0 " + cx + " " + (cy + innerRadius) +
      " A " + innerRadius + " " + innerRadius + " 0 1 0 " + cx + " " + (cy - innerRadius) + " Z";
  }

  function donutSlicePath(cx, cy, outerRadius, innerRadius, startAngle, endAngle) {
    var outerStart;
    var outerEnd;
    var innerStart;
    var innerEnd;
    var largeArc;
    if (endAngle - startAngle > Math.PI * 2 - 0.0001) {
      return fullDonutPath(cx, cy, outerRadius, innerRadius);
    }
    outerStart = polar(cx, cy, outerRadius, startAngle);
    outerEnd = polar(cx, cy, outerRadius, endAngle);
    innerStart = polar(cx, cy, innerRadius, startAngle);
    innerEnd = polar(cx, cy, innerRadius, endAngle);
    largeArc = endAngle - startAngle > Math.PI ? 1 : 0;
    return "M " + outerStart.x + " " + outerStart.y +
      " A " + outerRadius + " " + outerRadius + " 0 " + largeArc + " 1 " + outerEnd.x + " " + outerEnd.y +
      " L " + innerEnd.x + " " + innerEnd.y +
      " A " + innerRadius + " " + innerRadius + " 0 " + largeArc + " 0 " + innerStart.x + " " + innerStart.y + " Z";
  }

  function categoryTotals(rows) {
    var totals = [];
    var i;
    var j;
    var found;
    for (i = 0; i < rows.length; i += 1) {
      found = -1;
      for (j = 0; j < totals.length; j += 1) {
        if (totals[j].category === rows[i].categoria) {
          found = j;
          break;
        }
      }
      if (found === -1) {
        totals.push({ category: rows[i].categoria, quantity: Number(rows[i].quantidade) });
      } else {
        totals[found].quantity += Number(rows[i].quantidade);
      }
    }
    totals.sort(function (a, b) { return b.quantity - a.quantity; });
    return totals;
  }

  /* O donut usa a cidade como contexto; a categoria selecionada filtra o detalhe e o mês. */
  function drawDonut(cityRows, selectedCategory) {
    var totals = categoryTotals(cityRows);
    var grandTotal = 0;
    var colors = currentChartColors();
    var svg = makeSvg(
      byId("grafico-categoria"),
      "Itens vendidos por categoria. Selecione uma fatia ou use a legenda para filtrar.",
      "titulo-svg-categoria",
      "0 0 240 230"
    );
    var legend = byId("legenda-categoria");
    var cx = 116;
    var cy = 112;
    var outerRadius = 82;
    var innerRadius = 51;
    var angle = -Math.PI / 2;
    var i;
    var start;
    var end;
    var path;
    var button;
    var swatch;
    var label;
    var amount;
    var self;

    for (i = 0; i < totals.length; i += 1) {
      grandTotal += totals[i].quantity;
    }
    clearNode(legend);
    if (!grandTotal) {
      svg.appendChild(svgNode("text", { x: cx, y: cy, "text-anchor": "middle" }, "Sem dados"));
      setText(byId("categoria-ativa"), "Visão geral sem itens nesta cidade.");
      return;
    }

    for (i = 0; i < totals.length; i += 1) {
      start = angle;
      end = angle + Math.PI * 2 * totals[i].quantity / grandTotal;
      path = svgNode("path", {
        d: donutSlicePath(cx, cy, outerRadius, innerRadius, start, end),
        fill: colors[i % colors.length],
        "fill-rule": "evenodd",
        "class": "segmento" + (selectedCategory === totals[i].category ? " selecionado" : ""),
        "data-categoria": totals[i].category,
        tabindex: "0",
        role: "button",
        "aria-pressed": selectedCategory === totals[i].category ? "true" : "false",
        "aria-label": totals[i].category + ": " + formatInteger(totals[i].quantity) + " itens vendidos"
      });
      path.appendChild(svgNode("title", {}, totals[i].category + ": " + formatInteger(totals[i].quantity) + " itens"));
      self = totals[i].category;
      path.onclick = (function (category) {
        return function () { chooseCategory(category); };
      }(self));
      path.onkeydown = (function (category) {
        return function (event) {
          event = event || window.event;
          if (event.key === "Enter" || event.key === " " || event.keyCode === 13 || event.keyCode === 32) {
            if (event.preventDefault) event.preventDefault();
            chooseCategory(category);
          }
        };
      }(self));
      svg.appendChild(path);
      angle = end;

      button = document.createElement("button");
      button.type = "button";
      button.className = "legenda-item" + (selectedCategory === totals[i].category ? " selecionado" : "");
      button.setAttribute("data-categoria", totals[i].category);
      button.setAttribute("aria-pressed", selectedCategory === totals[i].category ? "true" : "false");
      swatch = document.createElement("span");
      swatch.className = "legenda-cor";
      swatch.style.backgroundColor = colors[i % colors.length];
      swatch.setAttribute("aria-hidden", "true");
      button.appendChild(swatch);
      label = document.createElement("span");
      label.appendChild(document.createTextNode(totals[i].category));
      button.appendChild(label);
      amount = document.createElement("strong");
      amount.className = "legenda-valor";
      amount.appendChild(document.createTextNode(formatInteger(totals[i].quantity)));
      button.appendChild(amount);
      self = totals[i].category;
      button.onclick = (function (category) {
        return function () { chooseCategory(category); };
      }(self));
      legend.appendChild(button);
    }
    svg.appendChild(svgNode("text", { x: cx, y: cy - 1, "text-anchor": "middle", "class": "centro-total" }, formatInteger(grandTotal)));
    svg.appendChild(svgNode("text", { x: cx, y: cy + 17, "text-anchor": "middle", "class": "centro-rotulo" }, "itens vendidos"));
    setText(byId("categoria-ativa"), selectedCategory ? "Categoria selecionada: " + selectedCategory + "." : "Visão geral de todas as categorias.");
  }

  function monthlyTotals(rows) {
    var totals = [];
    var month;
    var found;
    var i;
    var j;
    for (i = 0; i < rows.length; i += 1) {
      month = rows[i].data.substring(0, 7);
      found = -1;
      for (j = 0; j < totals.length; j += 1) {
        if (totals[j].month === month) {
          found = j;
          break;
        }
      }
      if (found === -1) {
        totals.push({ month: month, quantity: Number(rows[i].quantidade) });
      } else {
        totals[found].quantity += Number(rows[i].quantidade);
      }
    }
    totals.sort(function (a, b) { return a.month < b.month ? -1 : (a.month > b.month ? 1 : 0); });
    return totals;
  }

  function drawMonthlyColumns(rows) {
    var totals = monthlyTotals(rows);
    var maxQuantity = 1;
    var svg = makeSvg(
      byId("grafico-tempo"),
      "Quantidade de itens vendidos por mês" + (byId("filtro-categoria").value ? " na categoria " + byId("filtro-categoria").value : " em todas as categorias"),
      "titulo-svg-tempo",
      "0 0 560 250"
    );
    var colors = currentChartColors();
    var left = 55;
    var right = 18;
    var top = 24;
    var bottom = 202;
    var plotWidth = 560 - left - right;
    var plotHeight = bottom - top;
    var i;
    var y;
    var step;
    var barWidth;
    var x;
    var height;
    var label;
    var bar;

    for (i = 0; i < totals.length; i += 1) {
      if (totals[i].quantity > maxQuantity) maxQuantity = totals[i].quantity;
    }
    for (i = 0; i < 3; i += 1) {
      y = bottom - (i / 2) * plotHeight;
      svg.appendChild(svgNode("line", { x1: left, y1: y, x2: 542, y2: y, "class": "eixo" }));
      svg.appendChild(svgNode("text", { x: left - 8, y: y + 4, "text-anchor": "end" }, formatInteger(maxQuantity * i / 2)));
    }

    if (!totals.length) {
      svg.appendChild(svgNode("text", { x: 290, y: 125, "text-anchor": "middle" }, "Sem dados para exibir"));
      return;
    }
    step = plotWidth / totals.length;
    barWidth = Math.min(76, step * 0.52);
    for (i = 0; i < totals.length; i += 1) {
      height = totals[i].quantity / maxQuantity * plotHeight;
      x = left + i * step + (step - barWidth) / 2;
      y = bottom - height;
      label = MONTHS[Number(totals[i].month.substring(5, 7)) - 1] + " " + totals[i].month.substring(0, 4);
      bar = svgNode("rect", {
        x: x,
        y: y,
        width: barWidth,
        height: height,
        rx: 3,
        fill: colors[0],
        "class": "coluna",
        tabindex: "0",
        "aria-label": label + ": " + formatInteger(totals[i].quantity) + " itens vendidos"
      });
      bar.appendChild(svgNode("title", {}, label + ": " + formatInteger(totals[i].quantity) + " itens vendidos"));
      svg.appendChild(bar);
      svg.appendChild(svgNode("text", { x: x + barWidth / 2, y: Math.max(top - 3, y - 7), "text-anchor": "middle", "class": "valor-coluna" }, formatInteger(totals[i].quantity)));
      svg.appendChild(svgNode("text", { x: x + barWidth / 2, y: 225, "text-anchor": "middle" }, MONTHS[Number(totals[i].month.substring(5, 7)) - 1]));
    }
  }

  function clearNode(node) {
    while (node.firstChild) {
      node.removeChild(node.firstChild);
    }
  }

  function fillFilter(select, values, firstLabel) {
    var unique = [];
    var option;
    var i;
    var j;
    var found;
    while (select.options.length > 1) select.remove(1);
    select.options[0].value = "";
    setText(select.options[0], firstLabel);
    for (i = 0; i < values.length; i += 1) {
      found = false;
      for (j = 0; j < unique.length; j += 1) {
        if (unique[j] === values[i]) found = true;
      }
      if (!found) unique.push(values[i]);
    }
    unique.sort(function (a, b) {
      a = String(a).toLowerCase();
      b = String(b).toLowerCase();
      return a < b ? -1 : (a > b ? 1 : 0);
    });
    for (i = 0; i < unique.length; i += 1) {
      option = document.createElement("option");
      option.value = unique[i];
      option.appendChild(document.createTextNode(unique[i]));
      select.appendChild(option);
    }
  }

  function listen(node, eventName, handler) {
    if (node.addEventListener) node.addEventListener(eventName, handler, false);
    else if (node.attachEvent) node.attachEvent("on" + eventName, handler);
  }

  function getCityRows() {
    var city = byId("filtro-cidade").value;
    var rows = [];
    var i;
    for (i = 0; i < rowsAll.length; i += 1) {
      if (!city || rowsAll[i].cidade === city) rows.push(rowsAll[i]);
    }
    return rows;
  }

  /* A filtragem por cidade/categoria é aplicada em conjunto ao detalhe e ao gráfico mensal. */
  function render() {
    var city = byId("filtro-cidade").value;
    var category = byId("filtro-categoria").value;
    var cityRows = getCityRows();
    var detailRows = [];
    var totalValue = 0;
    var i;
    var row;
    var table = byId("corpo-tabela");
    var tr;
    var cell;
    var dateParts;
    var values;
    for (i = 0; i < cityRows.length; i += 1) {
      if (!category || cityRows[i].categoria === category) {
        detailRows.push(cityRows[i]);
        totalValue += Number(cityRows[i].valor_venda);
      }
    }

    setText(byId("kpi-total"), formatMoney(totalValue));
    setText(byId("kpi-vendas"), formatInteger(detailRows.length));
    setText(byId("kpi-ticket"), formatMoney(detailRows.length ? totalValue / detailRows.length : 0));
    if (detailRows.length) byId("estado-vazio").setAttribute("hidden", "hidden");
    else byId("estado-vazio").removeAttribute("hidden");
    setText(byId("resumo-filtros"), formatInteger(detailRows.length) + (detailRows.length === 1 ? " venda exibida" : " vendas exibidas"));
    setText(byId("contador-tabela"), formatInteger(detailRows.length) + (detailRows.length === 1 ? " venda" : " vendas"));
    drawDonut(cityRows, category);
    drawMonthlyColumns(detailRows);

    clearNode(table);
    for (i = 0; i < detailRows.length; i += 1) {
      row = detailRows[i];
      dateParts = row.data.split("-");
      values = [dateParts[2] + "/" + dateParts[1] + "/" + dateParts[0], row.id_venda, row.cidade, row.categoria, row.produto, formatInteger(row.quantidade), formatMoney(row.valor_venda)];
      tr = document.createElement("tr");
      for (var column = 0; column < values.length; column += 1) {
        cell = document.createElement("td");
        if (column >= 5) cell.className = "numero";
        cell.appendChild(document.createTextNode(String(values[column])));
        tr.appendChild(cell);
      }
      table.appendChild(tr);
    }
  }

  function chooseCategory(category) {
    var filter = byId("filtro-categoria");
    filter.value = filter.value === category ? "" : category;
    render();
  }

  function getSavedTheme() {
    try {
      return window.localStorage.getItem("papelaria-tema") === "escuro" ? "escuro" : "claro";
    } catch (error) {
      return "claro";
    }
  }

  /* A persistência é opcional por segurança: alguns navegadores restringem localStorage em file://. */
  function setTheme(theme, persist) {
    var dark = theme === "escuro";
    document.body.className = dark ? "tema-escuro" : "tema-claro";
    byId("alternar-tema").setAttribute("aria-pressed", dark ? "true" : "false");
    setText(byId("alternar-tema"), dark ? "Ativar tema claro" : "Ativar tema escuro");
    if (persist) {
      try {
        window.localStorage.setItem("papelaria-tema", dark ? "escuro" : "claro");
      } catch (error) {
        /* O tema continua funcionando nesta sessão mesmo se o navegador bloquear o armazenamento. */
      }
    }
    if (rowsAll.length) render();
  }

  function start() {
    var dataNode = byId("dashboard-data");
    var cityValues = [];
    var categoryValues = [];
    var i;
    try {
      rowsAll = JSON.parse(dataNode.textContent || dataNode.innerText || dataNode.text);
      if (!rowsAll || Object.prototype.toString.call(rowsAll) !== "[object Array]") {
        throw new Error("O JSON embutido precisa conter uma lista de vendas.");
      }
      for (i = 0; i < rowsAll.length; i += 1) {
        cityValues.push(rowsAll[i].cidade);
        categoryValues.push(rowsAll[i].categoria);
      }
      fillFilter(byId("filtro-cidade"), cityValues, "Todas as cidades");
      fillFilter(byId("filtro-categoria"), categoryValues, "Todas as categorias");
      listen(byId("filtro-cidade"), "change", render);
      listen(byId("filtro-categoria"), "change", render);
      listen(byId("limpar-filtros"), "click", function () {
        byId("filtro-cidade").value = "";
        byId("filtro-categoria").value = "";
        render();
        byId("filtro-cidade").focus();
      });
      listen(byId("voltar-visao-geral"), "click", function () {
        byId("filtro-categoria").value = "";
        render();
        byId("filtro-categoria").focus();
      });
      listen(byId("alternar-tema"), "click", function () {
        setTheme(document.body.className.indexOf("tema-escuro") !== -1 ? "claro" : "escuro", true);
      });
      setTheme(getSavedTheme(), false);
      render();
    } catch (error) {
      byId("estado-vazio").removeAttribute("hidden");
      setText(byId("estado-vazio"), "Não foi possível ler os dados embutidos. Execute preparar_dados.py novamente.");
      if (window.console && window.console.error) window.console.error("Não foi possível iniciar o painel:", error);
    }
  }

  start();
}());
