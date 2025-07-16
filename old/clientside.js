window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        getWindowSize: function(_) {
            return {
                width: window.innerWidth,
                height: window.innerHeight
            };
        },
        fitCytoscape: function(_) {
            const cyto = window.dash_clientside.cytoscapeInstances?.diagram;
            if (cyto) {
                cyto.fit();  // Centraliza automaticamente
            }
            return window.dash_clientside.no_update; // Para não alterar o zoom
        }
    }
});


(function() {
    function sendSize() {
        const event = new CustomEvent("window-resize", {
            detail: {
                width: window.innerWidth,
                height: window.innerHeight
            }
        });
        window.dispatchEvent(event);
    }
    window.addEventListener('resize', sendSize);
    window.addEventListener('load', sendSize);
})();