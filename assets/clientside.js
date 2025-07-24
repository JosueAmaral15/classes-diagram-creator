// Função de precisão
function precisionFunction(x, expoent) {
    const pow = Math.pow(10, -expoent);
    const term1 = x * Math.floor(0.5 * (Math.abs(x - pow + 1) - Math.abs(x - pow) + 1));
    const term2 = x * Math.floor(0.5 * (Math.abs(x + pow + 1) - Math.abs(x + pow) + 1));
    return term1 - term2 + x;
}

// Seno com entrada em graus
function angleRadiusSin(x) {
    return Math.sin(Math.PI * x / 180);
}

// Seno com precisão ajustada
function angleRadiusSinOptimized(x) {
    return precisionFunction(angleRadiusSin(x), 6);
}

// Cosseno com entrada em graus
function angleRadiusCos(x) {
    return Math.cos(Math.PI * x / 180);
}

// Cosseno com precisão ajustada
function angleRadiusCosOptimized(x) {
    return precisionFunction(angleRadiusCos(x), 6);
}

function euclideanDistance(x1, y1, x2, y2) {
  return Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
}

function larger_string_size(list){
    let max = 0;
    list.forEach(function(item){
        if(item.length > max){
            max = item.length;
        }
    });
    return max;
}
function wrapLabel(text, maxCharsPerLine = 40) {
  return text
    .split('\n')  // já existentes
    .map(line =>
      line.length > maxCharsPerLine
        ? line.match(new RegExp('.{1,' + maxCharsPerLine + '}', 'g')).join('\n')
        : line
    )
    .join('\n');
}

function highlightTextStandalone(node, searchTerm, search_type) {
    const label = node.data('label');
    const lines = label.split('\n');
    total_lines = lines.length;
    const fontSize = parseFloat(node.style('font-size')) || 10;
    const charWidth = fontSize;
    const lineHeight = fontSize;
    //const padding = (parseFloat(node.style('padding')) || 5);
    const nodeWidth = node.width();
    const nodeHeight = node.height();
    const baseX = node.position('x');
    const baseY = node.position('y');
    node.style({'events' : 'no'});
    const groupId = 'group_' + node.id();
     
    if (!cy.getElementById(groupId).nonempty()) {
        cy.add({
            group: 'nodes',
            data: { id: groupId },
            classes: 'invisible'
        });
    }
    node.move({ parent: groupId });

    const highlights = [];

    lines.forEach((line, lineIndex) => {
        const regex = new RegExp(searchTerm, 'gi');
        let match;
        
        //debugLog(`DEBUG 83 before: search_type: ${search_type}, lineIndex: ${lineIndex}`);
        if (!search_type && lineIndex != 0) {
            return;
        }

        //debugLog(`DEBUG 83 after: search_type: ${search_type}, lineIndex: ${lineIndex}`);
        
        while ((match = regex.exec(line)) !== null) {
            const columnIndex = match.index;
            const centerLine = Math.floor(lines.length / 2);
            const max_column = Math.max(...lines.map(l => l.length));
            const centerColumn = max_column / 2;
            const firstPositionX = (nodeWidth -max_column*4.805)/2;
            const firstPositionY = (nodeHeight -total_lines*8.4375) /2; // Verificar se realmente está certo
            const offsetX = columnIndex * charWidth*0.6;
            const offsetY = lineIndex  * lineHeight*1.05;
            const resultX = baseX -nodeWidth/2 +firstPositionX +offsetX;
            const resultY = baseY -nodeHeight/2 +firstPositionY +offsetY;
            //debugLog(`columnIndex: ${columnIndex}, charWidth: ${charWidth}, lineIndex: ${lineIndex}, lineHeight: ${lineHeight}, centerLine: ${centerLine}, max_column: ${max_column}, centerColumn: ${centerColumn}, firstPositionX: ${firstPositionX}, firstPositionY: ${firstPositionY}, offsetX: ${offsetX}, offsetY: ${offsetY}, resultX: ${resultX}, resultY: ${resultY}.`);
            highlights.push({
                id: `highlight_${node.id()}_${highlights.length}`,
                text: match[0],
                x: resultX,
                y: resultY
            });
        }
    });

    cy.getElementById(groupId).data('highlight_elements_quantity', highlights.length);

    highlights.forEach(({ id, text, x, y }) => {
        if (cy.getElementById(id).nonempty()) cy.getElementById(id).remove();

        const highlightNode = cy.add({
            group: 'nodes',
            data: {
                id: id,
                label: text,
                fontSize : fontSize
            },
            position: { x, y },
            grabbable: false,
            selectable: false,
            classes: 'highlight'
        });

        highlightNode.move({ parent: groupId });
    });
}

function clearTextHighlights() {
    cy.nodes().forEach(node => {
        node.style({'events' : 'yes'});
        const group = cy.getElementById('group_' + node.id());
        const quantity = group.data('highlight_elements_quantity');
        for (let i = 0; i < quantity; i++) {
            const highlight = cy.getElementById('highlight_' + node.id() + '_' + i);
            if (highlight.nonempty()) highlight.remove();
        }
        if (group.nonempty()) node.move({ parent: null });
        if (group.nonempty()) group.remove();
    });
}

// function clearTextHighlights(cy) {
//   cy.nodes('.highlight').remove();
// }

function highlightNode(node) {
    node.style({
        'background-color': '#A2B0BB',
        'border-color': '#777777',
        'border-width': 2
    });
}

function resetNodeStyle(node) {
    node.style({
        'background-color': '#E6F2FF',
        'border-color': '#000',
        'border-width': 1
    });
}

function debugLog(msg) {
    const el = document.getElementById('debug-output');
    if (el) {
        el.innerText += msg + '\n';
    }
}

window.dash_clientside.latestKeyPressed = null;

document.addEventListener("keydown", function(e) {
    if (!["PageDown", "PageUp", "Enter", "Escape"].includes(e.key)) return;
    window.dash_clientside.latestKeyPressed = e.key;
});

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        restoreInitialView: function(n_clicks) {
            const cy = window.dash_clientside.cytoscapeInstances?.diagram;
            if (!cy) {
                //debugLog("⚠️ Cytoscape ainda não está pronto");
                return window.dash_clientside.no_update;
            }

            // Zoom padrão
            cy.zoom(1);

            // Pan padrão: baseado no centro do grafo (assumido como o node invisível "anchor")
            const anchor = cy.getElementById("anchor");
            if (!anchor || anchor.empty()) {
                //debugLog("⚠️ Anchor não encontrado. Centralizando por fit().");
                cy.fit();
                return window.dash_clientside.no_update;
            }

            // Calcula o deslocamento do anchor até o centro da tela
            const rendered = anchor.renderedPosition();
            const viewport = cy.container().getBoundingClientRect();

            const deltaX = rendered.x - viewport.width / 2;
            const deltaY = rendered.y - viewport.height / 2;

            const currentPan = cy.pan();
            const adjustedPan = {
                x: currentPan.x - deltaX,
                y: currentPan.y - deltaY
            };

            cy.pan(adjustedPan);
            clearTextHighlights(cy);
            cy.nodes().forEach(element => {
                resetNodeStyle(element); // estilo padrão
            });

            //debugLog("✅ View restaurada com zoom=1 e pan recalibrado:", adjustedPan);
            return window.dash_clientside.no_update;
        },
        pollKeyEvent: function(n_intervals) {
            const key = window.dash_clientside.latestKeyPressed || null;
            if (!key) return window.dash_clientside.no_update;
            // Zera após enviar para não enviar repetidamente
            window.dash_clientside.latestKeyPressed = null;
            return { key: key, timestamp: Date.now() };
        },
        highlightAndNavigate: function (n_clicks, n_submit, keyEventStore, matchType, search_type, searchText, prevStore) {
            
            const cy = window.dash_clientside.cytoscapeInstances?.diagram;
            if (!cy) return window.dash_clientside.no_update;
            
            const term = (searchText || '').trim().toLowerCase();
            if (!term) return window.dash_clientside.no_update;
            
            const keyEvent = keyEventStore?.key || null;
            //debugLog(`keyEvent: ${keyEvent}`);
            const ctx = dash_clientside.callback_context;
            const triggered = ctx.triggered.map(t => t.prop_id)[0];
            let results = prevStore?.results || [];
            let currentIndex = prevStore?.currentIndex || 0;
            
            if (triggered === 'btn-search.n_clicks' || ["PageDown", "PageUp"].includes(keyEvent) || ["search-input.n_submit"].includes(triggered)) {

                results = [];
                
                clearTextHighlights(cy); // restaura os textos

                cy.nodes().forEach(ele => {
                    const label = (ele.data('label') || '').toLowerCase();
                    const match = matchType === 'exata' ? label === term : label.includes(term);
                    //const lines = label.split('\n');
                    //const match_scope = search_type === 'all'? true : lines[0].includes(term);
                    //debugLog(`match_scope: ${match_scope}, match: ${match}, label: ${label}, term: ${term}, lines: ${lines[0]}, search_type: ${search_type}, label: ${label}`);
                    //const finalMatch = match && match_scope;
                    if (match) {
                        highlightTextStandalone(ele, term, search_type === 'all'); // muda apenas o texto com <span>
                        highlightNode(ele); // aplica estilo visual
                        results.push(ele.id());
                    } else {
                        resetNodeStyle(ele); // estilo padrão
                    }
                });

                if (results.length > 0) {
                    //currentIndex = (currentIndex + 1) % results.length;
                    if (keyEvent === "PageUp") {
                            currentIndex = (currentIndex - 1 + results.length) % results.length;
                        } else {
                            currentIndex = (currentIndex + 1) % results.length;
                        }
                    const node = cy.getElementById(results[currentIndex]);
                    if (node && !node.empty()) {
                        const subElementNode = cy.getElementById('highlight_' + node.id() + '_' + 0);
                        if (subElementNode) {
                            cy.animate({ center: { eles:  subElementNode}, zoom: 1.5 });
                        }
                    }
                } else {
                    currentIndex = 0;
                }
            } else if (["Escape"].includes(keyEvent)) {
                clearTextHighlights(cy);
                cy.nodes().forEach(element => {
                    resetNodeStyle(element); // estilo padrão
                });
            }
            return { results, currentIndex };
        },
        trackMousePosition: function () {
            const cy = window.dash_clientside.cytoscapeInstances?.diagram;
            if (!cy) {
                //debugLog("⚠️ Cytoscape ainda não está pronto");
                return window.dash_clientside.no_update;
            }
            //debugLog("⚠️ Acionado!");
            cy.on('mousemove', function (event) {
                //debugLog("⚠️ executando...");
                const pos = event.position;
                if (pos) {
                const output = `X: ${pos.x.toFixed(2)}, Y: ${pos.y.toFixed(2)}`;
                const div = document.getElementById('mouse-coords');
                if (div) div.innerText = output;
                }
            });

        return '';
        }
    }
});

(function waitForCytoscapeInstance() {
    const cyElement = document.getElementById('diagram');
    if (cyElement && cyElement._cyreg && typeof cyElement._cyreg.cy === "object") {
        //debugLog("✅ window.dash_clientside.cytoscapeInstances.diagram registrado com sucesso");
        window.dash_clientside = window.dash_clientside || {};
        window.dash_clientside.clientside = window.dash_clientside.clientside || {};
        window.dash_clientside.cytoscapeInstances = window.dash_clientside.cytoscapeInstances || {};
        window.dash_clientside.cytoscapeInstances.diagram = cyElement._cyreg.cy;

        //debugLog('✅ Cytoscape instância registrada manualmente via polling');
    } else {
        //debugLog('? cy não está pronto ainda (aguardando...)');
        setTimeout(waitForCytoscapeInstance, 250); // tenta de novo em 250ms
    }
})();