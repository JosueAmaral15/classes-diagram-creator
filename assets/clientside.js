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

function highlightTextStandalone(node, searchTerm) {
    const label = node.data('label');
    const match = label.match(new RegExp(searchTerm, 'i'));
    if (!match) return;

    const matchText = match[0];
    const highlightId = 'highlight_' + node.id();
    const groupId = 'group_' + node.id();

    const existing = cy.getElementById(highlightId);
    if (existing.nonempty()) existing.remove();

    if (!cy.getElementById(groupId).nonempty()) {
        cy.add({ group: 'nodes', data: { id: groupId }, classes: 'invisible' });
    }

    const index = label.toLowerCase().indexOf(matchText.toLowerCase());
    let line_breaks = label.match(/\n/g);
    const total_line_breaks_quantity = line_breaks ? line_breaks.length : 0;
    const total_lines = total_line_breaks_quantity +1;
    const center_lines = Math.floor(total_lines / 2);
    //Como para cada linha existe uma quantidade de caracteres limitada de acordo com o tamanho definido pelo node.width(), isto quer dizer que, para cada linha, o texto pode ser dividido em N partes
    const substring = label.substring(0,index);
    line_breaks = substring.match(/\n/g);
    const quantity_line_breaks = line_breaks ? line_breaks.length : 0; 
    const current_line = quantity_line_breaks;
    const parts = label.split('\n');
    const current_line_string = parts[quantity_line_breaks];
    const current_column = current_line_string.toLowerCase().indexOf(matchText.toLowerCase());
    const greater_column_length = larger_string_size(parts);
    const center_column = greater_column_length /2;
    const font_size = parseFloat(node.style('font-size'));
    // const center_point = cy.getElementById('anchor');
    // const position = center_point.position();
    // const center_x = position.x;
    // const center_y = position.y;
    // const initial_current_element_place_X = node.position('x') -node.width()/2;
    // const initial_current_element_place_Y = node.position('y') -node.height()/2;
    const factor = 1;
    
    const horizontal_string_length = font_size * Math.abs(center_column -current_column); 
    
    const vertical_string_length = font_size * Math.abs(center_lines - current_line);

    const current_point_X = node.position('x') +(matchText != current_line_string?  horizontal_string_length * (center_column - current_column != 0? (center_column - current_column < 0? 1 : -1) : 0) : 0);

    const current_point_Y = node.position('y') +(total_lines != current_line? vertical_string_length *(center_lines != current_line? (center_lines -current_line < 0? 1 : -1) : 0) : 0);

    const horizontal_string_position =  0; //horizontal_string_position;
    const vertical_string_position = 0; //vertical_string_position;
    const distance = 0; // euclideanDistance(node.position('x'), node.position('y'), current_point_X, current_point_Y);
    const angle = 0; // Math.atan2(current_point_Y -node.position('y'), current_point_X -node.position('x'));
    if (label == "FUNC_BENEFICIO")
        debugLog(`index: ${index}, line_breaks: ${line_breaks}, total_line_breaks_quantity: ${total_line_breaks_quantity}, total_lines: ${total_lines}, center_lines: ${center_lines}, substring: ${substring}, quantity_line_breaks: ${quantity_line_breaks}, current_line: ${current_line}, parts: ${parts}, current_line_string: ${current_line_string}, current_column: ${current_column}, center_column: ${center_column}, font_size: ${font_size}, horizontal_string_length: ${horizontal_string_length}, vertical_string_length: ${vertical_string_length}, horizontal_string_position: ${horizontal_string_position}, vertical_string_position: ${vertical_string_position}, current_point_X: ${current_point_X}, current_point_Y: ${current_point_Y}, node.position('x'): ${node.position('x')}, node.position('Y'): ${node.position('x')}, distance: ${distance}, angle: ${angle}.`)
    node.style('events', 'no');
    node.move({ parent: groupId });

    const highlightNode = cy.add({
        group: 'nodes',
        data: {
            id: highlightId,
            label: matchText  // agora será visível
        },
        position: {
            // x: node.position('x') +Math.cos(angle)*distance,
            // y: node.position('y') +Math.sin(angle)*distance
            x: current_point_X,
            y: current_point_Y
        },
        grabbable: false,
        selectable: false,
        classes: 'highlight'
    });

    highlightNode.move({ parent: groupId });
}


function clearTextHighlights() {
    cy.nodes().forEach(n => {
        const highlight = cy.getElementById('highlight_' + n.id());
        const group = cy.getElementById('group_' + n.id());

        // Remove apenas o destaque, mas move o node de volta à raiz
        if (highlight.nonempty()) highlight.remove();
        if (group.nonempty()) n.move({ parent: null });
        if (group.nonempty()) group.remove();  // remove grupo vazio
    });
}


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
        el.innerText = msg;
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
            clearTextHighlights()
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
        highlightAndNavigate: function (n_clicks, n_submit, keyEventStore, matchType, searchText, prevStore) {
            
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
                
                clearTextHighlights(); // restaura os textos

                cy.nodes().forEach(ele => {
                    const label = (ele.data('label') || '').toLowerCase();
                    const match = matchType === 'exata' ? label === term : label.includes(term);

                    if (match) {
                        highlightTextStandalone(ele, term); // muda apenas o texto com <span>
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
                        cy.animate({ center: { eles: node }, zoom: 1.5 });
                    }
                } else {
                    currentIndex = 0;
                }
            } else if (["Escape"].includes(keyEvent)) {
                clearTextHighlights()
                cy.nodes().forEach(element => {
                    resetNodeStyle(element); // estilo padrão
                });
            }
            return { results, currentIndex };
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