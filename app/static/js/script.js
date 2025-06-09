function actualizarEstado(selectElement, detalleId) {
    const nuevoEstado = selectElement.value;

    fetch("/actualizar_estado", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            detalle_id: detalleId,
            nuevo_estado: nuevoEstado
        })
    })
    .then(response => {
        if (response.ok) {
            selectElement.style.border = "2px solid green";
            setTimeout(() => selectElement.style.border = "", 1000);
        } else {
            alert("Error al actualizar estado");
        }
    });
}
