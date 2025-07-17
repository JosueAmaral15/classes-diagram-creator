function debugLog(msg) {
    const el = document.getElementById('debug-output');
    if (el) {
        el.innerText = msg;
    }
}

debugLog("📦 clientside.js carregado com sucesso");

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        restoreInitialView: function(n_clicks) {
            const cy = window.dash_clientside.cytoscapeInstances?.diagram;
            if (!cy) {
                debugLog("⚠️ Cytoscape ainda não está pronto");
                return window.dash_clientside.no_update;
            }

            // Zoom padrão
            cy.zoom(1);

            // Pan padrão: baseado no centro do grafo (assumido como o node invisível "anchor")
            const anchor = cy.getElementById("anchor");
            if (!anchor || anchor.empty()) {
                debugLog("⚠️ Anchor não encontrado. Centralizando por fit().");
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

            //debugLog("✅ View restaurada com zoom=1 e pan recalibrado:", adjustedPan);
            return window.dash_clientside.no_update;
        },
        // highlightSearchResults: function (n_clicks, searchText, matchType, storeData) {
        //     //debugLog("highlightSearchResults")
        //     const cy = window.dash_clientside.cytoscapeInstances?.diagram;
        //     debugLog(`searchText: ${searchText}, matchType: ${matchType}, storeData: ${storeData}, storeData.results.length: ${storeData.results.length}`)
        //     if (!cy || !searchText || !storeData) return window.dash_clientside.no_update;
        //     //debugLog("continue highlightSearchResults")
        //     let current = 0
        //     if (storeData.results.length > 0)
        //         current = storeData.currentIndex;
            
        //     debugLog(`Current: ${current}, searchText: ${searchText}, matchType: ${matchType}, storeData: ${storeData}, storeData.results.length: ${storeData.results.length}`)
        //     const term = searchText.trim().toLowerCase();
        //     if (!term) return window.dash_clientside.no_update;

        //     const matched = [];

        //     cy.elements().removeClass("highlight");

        //     cy.nodes().forEach(ele => {
        //         const label = (ele.data('label') || '').toLowerCase();
        //         const match = matchType === 'exata' ? label === term : label.includes(term);

        //         if (match) {
        //         ele.addClass("highlight");
        //         matched.push(ele.id());
        //         } else {
        //         ele.removeClass("highlight");
        //         }
        //     });

        //     return { results: matched, currentIndex: current};
        // },
        // highlightAndFocusResults: function (n_clicks, searchText, matchType) {
        //     const cy = window.dash_clientside.cytoscapeInstances?.diagram;
        //     if (!cy || !searchText) return window.dash_clientside.no_update;

        //     const term = searchText.trim().toLowerCase();
        //     if (!term) return window.dash_clientside.no_update;

        //     const matched = [];

        //     cy.elements().removeClass("highlight");

        //     cy.nodes().forEach(ele => {
        //         const label = (ele.data('label') || '').toLowerCase();
        //         const match = matchType === 'exata' ? label === term : label.includes(term);

        //         if (match) {
        //             ele.addClass("highlight");
        //             matched.push(ele.id());
        //         } else {
        //             ele.removeClass("highlight");
        //         }
        //     });

        //     if (matched.length === 0) return { results: [], currentIndex: 0 };

        //     const first = cy.getElementById(matched[0]);
        //     if (first && !first.empty()) {
        //         cy.animate({
        //             center: { eles: first },
        //             zoom: 1.5
        //         });
        //     }

        //     return { results: matched, currentIndex: 0 };
        // },
        highlightAndNavigate: function (n_clicks, n_submit, searchText, matchType, prevStore) {
            const cy = window.dash_clientside.cytoscapeInstances?.diagram;
            if (!cy) return window.dash_clientside.no_update;

            const ctx = dash_clientside.callback_context;
            const triggered = ctx.triggered.map(t => t.prop_id)[0];

            const term = (searchText || '').trim().toLowerCase();
            if (!term) return window.dash_clientside.no_update;

            let results = prevStore?.results || [];
            let currentIndex = prevStore?.currentIndex || 0;

            if (triggered === 'btn-search.n_clicks') {
                results = [];
                cy.elements().removeClass("highlight");

                cy.nodes().forEach(ele => {
                    const label = (ele.data('label') || '').toLowerCase();
                    const match = matchType === 'exata' ? label === term : label.includes(term);

                    if (match) {
                        ele.addClass("highlight");
                        results.push(ele.id());
                    } else {
                        ele.removeClass("highlight");
                    }
                });
                
                if (results.length > 0) {
                    currentIndex = (currentIndex + 1) % results.length;
                    const node = cy.getElementById(results[currentIndex]);
                    if (node && !node.empty()) {
                        cy.animate({ center: { eles: node }, zoom: 1.5 });
                    }
                } else {
                    currentIndex = 0;
                }

            } else if (["search-input.n_submit"].includes(triggered)) {
                if (!results.length) return window.dash_clientside.no_update;

                currentIndex = (currentIndex + 1) % results.length;
                const node = cy.getElementById(results[currentIndex]);
                if (node && !node.empty()) {
                    cy.animate({ center: { eles: node }, zoom: 1.5 });
                }
            }

            return { results, currentIndex };
        },
        // focusCurrentResult: function (keyEvent, n_clicks, storeData) {
        // const cy = window.dash_clientside.cytoscapeInstances?.diagram;
        // if (!cy || !storeData || !storeData.results.length) return window.dash_clientside.no_update;

        // let current = storeData.currentIndex;
        // const total = storeData.results.length;

        // // if (["PageDown", "Enter"].includes(keyEvent)) {
        // //     current = (current + 1) % total;
        // if (keyEvent === "PageUp") {
        //     current = (current - 1 + total) % total;
        // } else {
        //     current = (current + 1) % total;
        // }

        // const idToFocus = storeData.results[current];
        // const node = cy.getElementById(idToFocus);
        // if (node && !node.empty()) {
        //     cy.animate({
        //     center: { eles: node },
        //     zoom: 1.5
        //     });
        // }
        // //debugLog(`currentIndex: ${current}, storeData.results.length: ${storeData.results.length}, idToFocus: ${idToFocus}`);
        // return { results: storeData.results, currentIndex: current };
        // }
    }
});

(function waitForCytoscapeInstance() {
    const cyElement = document.getElementById('diagram');
    if (cyElement && cyElement._cyreg && typeof cyElement._cyreg.cy === "object") {
        //debugLog("✅ window.dash_clientside.cytoscapeInstances.diagram registrado com sucesso");
        window.dash_clientside = window.dash_clientside || {};
        window.dash_clientside.cytoscapeInstances = window.dash_clientside.cytoscapeInstances || {};
        window.dash_clientside.cytoscapeInstances.diagram = cyElement._cyreg.cy;

        //debugLog('✅ Cytoscape instância registrada manualmente via polling');
    } else {
        //debugLog('? cy não está pronto ainda (aguardando...)');
        setTimeout(waitForCytoscapeInstance, 250); // tenta de novo em 250ms
    }
})();

