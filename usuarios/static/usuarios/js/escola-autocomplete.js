document.querySelectorAll('.school-autocomplete').forEach((container) => {
    const input = container.querySelector('.school-search-input');
    const schoolField = container.querySelector('input[name="escola"]');
    const results = container.querySelector('#escola-results');
    const selection = container.querySelector('#escola-selection');
    let debounceTimer;
    let activeRequest;

    if (!input || !schoolField || !results || !selection) return;

    if (schoolField.dataset.selectedLabel) {
        input.value = schoolField.dataset.selectedLabel;
        selection.textContent = `Escola selecionada: ${schoolField.dataset.selectedLabel}`;
    }

    input.addEventListener('input', () => {
        window.clearTimeout(debounceTimer);
        if (activeRequest) activeRequest.abort();
        schoolField.value = '';
        delete schoolField.dataset.selectedLabel;
        results.replaceChildren();
        results.hidden = true;

        const term = input.value.trim();
        selection.textContent = term.length < 2
            ? 'Digite ao menos 2 caracteres para buscar.'
            : 'Buscando escolas...';
        if (term.length < 2) return;

        debounceTimer = window.setTimeout(async () => {
            activeRequest = new AbortController();
            try {
                const url = new URL(container.dataset.searchUrl, window.location.origin);
                url.searchParams.set('q', term);
                const response = await fetch(url, { signal: activeRequest.signal });
                if (!response.ok) throw new Error('Falha na busca de escolas.');
                const data = await response.json();
                results.replaceChildren();

                data.results.forEach((school) => {
                    const option = document.createElement('button');
                    option.type = 'button';
                    option.className = 'list-group-item list-group-item-action';
                    option.setAttribute('role', 'option');
                    option.textContent = school.label;
                    option.addEventListener('click', () => {
                        schoolField.value = school.id;
                        schoolField.dataset.selectedLabel = school.label;
                        input.value = school.label;
                        selection.textContent = `Escola selecionada: ${school.label}`;
                        results.replaceChildren();
                        results.hidden = true;
                    });
                    results.append(option);
                });

                results.hidden = data.results.length === 0;
                selection.textContent = data.results.length
                    ? `${data.results.length} resultado(s). Selecione uma escola.`
                    : 'Nenhuma escola encontrada.';
            } catch (error) {
                if (error.name !== 'AbortError') selection.textContent = error.message;
            }
        }, 250);
    });

    input.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') results.hidden = true;
    });
});