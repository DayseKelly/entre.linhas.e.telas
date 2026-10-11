(() => {
    const frames = document.querySelectorAll('[data-cover-title]');
    const cachePrefix = 'entre-linhas-capa-v4:';

    function normalize(value) {
        return String(value || '')
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .toLocaleLowerCase()
            .replace(/[^a-z0-9]+/g, ' ')
            .trim();
    }

    function authorMatches(foundAuthors, expectedAuthor) {
        const expectedNames = String(expectedAuthor || '').split(/\s+(?:e|&)\s+|,/i);
        const expectedTokens = normalize(expectedNames[0]).split(' ').filter((token) => token.length > 2);
        const authors = (foundAuthors || []).map(normalize);
        return expectedTokens.length > 0 && authors.some((author) => {
            const matchingTokens = expectedTokens.filter((token) => author.includes(token));
            return matchingTokens.length >= Math.min(2, expectedTokens.length);
        });
    }

    async function searchBook(title, author) {
        const query = new URLSearchParams({
            title,
            author: String(author || '').split(/\s+(?:e|&)\s+|,/i)[0],
            limit: '10',
            fields: 'cover_i,title,author_name',
        });
        const response = await fetch(`https://openlibrary.org/search.json?${query}`);
        if (!response.ok) return null;
        const data = await response.json();
        const expectedTitle = normalize(title);
        const book = data.docs?.find((item) => {
            const foundTitle = normalize(item.title);
            return item.cover_i && foundTitle === expectedTitle && authorMatches(item.author_name, author);
        });
        return book ? `https://covers.openlibrary.org/b/id/${book.cover_i}-L.jpg?default=false` : null;
    }

    async function searchMusic(title, author) {
        const titleWithoutArtist = title.split(/\s+[—–-]\s+/)[0];
        const query = new URLSearchParams({
            term: `${titleWithoutArtist} ${author}`,
            entity: 'song',
            limit: '10',
        });
        const response = await fetch(`https://itunes.apple.com/search?${query}`);
        if (!response.ok) return null;
        const data = await response.json();
        const expectedTitle = normalize(titleWithoutArtist);
        const track = data.results?.find((item) => {
            const foundTitle = normalize(item.trackName);
            return item.artworkUrl100 && foundTitle === expectedTitle && normalize(item.artistName).includes(normalize(String(author).split(/\s+e\s+|,/i)[0]));
        });
        return track?.artworkUrl100?.replace(/\/\d+x\d+bb\./, '/600x600bb.') || null;
    }

    async function searchWikipedia(title) {
        const verifiedPages = {
            'Her': ['Her (film)'],
            'O Auto da Compadecida': ['O Auto da Compadecida (filme)'],
            'Como Estrelas na Terra': ['Taare Zameen Par'],
            'Coach Carter': ['Coach Carter'],
            'Medida Provisória': ['Medida Provisória'],
            'Ailton Krenak': ['Ailton Krenak'],
            'Byung-Chul Han': ['Byung-Chul Han'],
            'Djamila Ribeiro': ['Djamila Ribeiro'],
            'Josué de Castro': ['Josué de Castro'],
            'Paulo Freire': ['Paulo Freire'],
            'Pelé': ['Pelé'],
            'Racionais MC’s': ['Racionais MCs'],
            'Sabotage': ['Sabotage (rapper)'],
            'Filipe Ret': ['Filipe Ret'],
        };
        const pageTitles = verifiedPages[title];
        if (!pageTitles) return null;
        for (const language of ['pt', 'en']) {
            for (const pageTitle of pageTitles) {
                const query = new URLSearchParams({
                    action: 'query',
                    titles: pageTitle,
                    prop: 'pageimages',
                    piprop: 'thumbnail',
                    pithumbsize: '700',
                    format: 'json',
                    origin: '*',
                    redirects: '1',
                });
                const response = await fetch(`https://${language}.wikipedia.org/w/api.php?${query}`);
                if (!response.ok) continue;
                const data = await response.json();
                const page = Object.values(data.query?.pages || {}).find((item) => item.thumbnail?.source);
                if (page) return page.thumbnail.source;
            }
        }
        return null;
    }

    async function findCover(frame) {
        const title = frame.dataset.coverTitle;
        const author = frame.dataset.coverAuthor || '';
        const type = (frame.dataset.coverType || '').toLocaleLowerCase();

        if (type.includes('música') && !type.includes('trajetória')) return searchMusic(title, author);
        if (type.includes('livro')) {
            return searchBook(title, author);
        }
        if (type !== 'legislação') return searchWikipedia(title);
        return null;
    }

    async function addRemoteCover(frame) {
        if (frame.dataset.coverLookup) return;
        frame.dataset.coverLookup = 'done';

        const fallback = frame.querySelector('[data-cover-fallback]');
        if (!fallback) return;

        const cacheKey = `${cachePrefix}${normalize(frame.dataset.coverTitle)}`;
        try {
            const cached = JSON.parse(localStorage.getItem(cacheKey));
            if (cached && cached.expires > Date.now()) {
                if (cached.source) {
                    const cachedImage = document.createElement('img');
                    cachedImage.dataset.coverImage = 'true';
                    cachedImage.alt = `Capa de ${frame.dataset.coverTitle}`;
                    cachedImage.className = 'cover-photo';
                    cachedImage.addEventListener('load', () => { fallback.hidden = true; }, { once: true });
                    cachedImage.addEventListener('error', () => { cachedImage.remove(); fallback.hidden = false; }, { once: true });
                    frame.insertBefore(cachedImage, fallback);
                    cachedImage.src = cached.source;
                }
                return;
            }
        } catch {
            localStorage.removeItem(cacheKey);
        }

        try {
            const source = await findCover(frame);
            localStorage.setItem(cacheKey, JSON.stringify({ source, expires: Date.now() + 30 * 24 * 60 * 60 * 1000 }));
            if (!source) return;

            const image = document.createElement('img');
            image.dataset.coverImage = 'true';
            image.alt = `Capa de ${frame.dataset.coverTitle}`;
            image.decoding = 'async';
            image.className = 'cover-photo';
            image.addEventListener('load', () => {
                if (image.naturalWidth > 1) fallback.hidden = true;
                else image.remove();
            }, { once: true });
            image.addEventListener('error', () => {
                image.remove();
                fallback.hidden = false;
                localStorage.setItem(cacheKey, JSON.stringify({ source: null, expires: Date.now() + 30 * 24 * 60 * 60 * 1000 }));
            }, { once: true });
            frame.insertBefore(image, fallback);
            image.src = source;
        } catch {
            fallback.hidden = false;
        }
    }

    function initializeFrame(frame) {
        const image = frame.querySelector('[data-cover-image]');
        const fallback = frame.querySelector('[data-cover-fallback]');
        if (!image) {
            addRemoteCover(frame);
            return;
        }

        const handleLoad = () => {
            if (image.naturalWidth > 1 && fallback) fallback.hidden = true;
        };
        const handleError = () => {
            image.remove();
            if (fallback) fallback.hidden = false;
            addRemoteCover(frame);
        };

        image.addEventListener('load', handleLoad, { once: true });
        image.addEventListener('error', handleError, { once: true });
        if (image.complete) {
            if (image.naturalWidth > 1) handleLoad();
            else handleError();
        }
    }

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            for (const entry of entries) {
                if (!entry.isIntersecting) continue;
                observer.unobserve(entry.target);
                initializeFrame(entry.target);
            }
        }, { rootMargin: '240px' });
        frames.forEach((frame) => observer.observe(frame));
    } else {
        frames.forEach(initializeFrame);
    }
})();