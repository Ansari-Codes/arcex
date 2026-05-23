async function axEvent(eventId, eventType, payload = {}) {
    try {
        const res = await fetch(`/.event/${eventId}/${eventType}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const datata = await res.json();

        if (!datata) return;

        for (const [id, data] of Object.entries(datata)) {
            const el = document.getElementById(id);

            switch (data.op) {

                case "replace":
                    if (!el) break;
                    el.outerHTML = data.html;
                    break;

                case "inner_replace":
                    if (!el) break;
                    el.innerHTML = data.html;
                    break;

                case "add":
                    if (el) break;
                    document.body.insertAdjacentHTML("beforeend", data.html);
                    break;

                case "remove":
                    if (el) el.remove();
                    break;

                case "value":
                    if (el) el.value = data.value;
                    break;
            }
        }
    } catch (err) {
        console.error("Ax Event Error:", err);
    }
}

function debounce(fn, delay = 300) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => fn(...args), delay);
    };
}

const axInputEvent = debounce((eventId, value) => {
    axEvent(eventId, "oninput", value);
}, 300);