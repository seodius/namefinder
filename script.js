document.addEventListener('DOMContentLoaded', () => {
    const app = document.getElementById('app');
    const state = {};
    const API_URL = 'http://127.0.0.1:5001';

    function renderStep1() {
        app.innerHTML = `
            <h2>Create a Catchy Company Name</h2>
            <form id="step1-form">
                <div class="form-group">
                    <label for="headline">Headline</label>
                    <input type="text" id="headline" placeholder="A single, attention-grabbing sentence that communicates the primary end-benefit." required>
                </div>
                <div class="form-group">
                    <label for="what">What</label>
                    <textarea id="what" placeholder="A 2-3 sentence paragraph that elaborates on what is being offered" required></textarea>
                </div>
                <div class="form-group">
                    <label for="for-who">For who</label>
                    <textarea id="for-who" placeholder="The target audience(s) and why it is useful." required></textarea>
                </div>
                <div class="form-group">
                    <label for="features">Features</label>
                    <textarea id="features" placeholder="Three to five key features or benefits in a scannable format." required></textarea>
                </div>
                <button type="submit">Get UVP</button>
            </form>
        `;

        document.getElementById('step1-form').addEventListener('submit', e => {
            e.preventDefault();
            state.headline = document.getElementById('headline').value;
            state.what = document.getElementById('what').value;
            state.forWho = document.getElementById('for-who').value;
            state.features = document.getElementById('features').value;

            fetch(`${API_URL}/api/uvp`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(state)
            })
            .then(response => response.json())
            .then(data => renderStep2(data.uvp))
            .catch(error => console.error('Error fetching UVP:', error));
        });
    }

    function renderStep2(uvp) {
        app.innerHTML = `
            <h2>Step 2: Validate Your Unique Value Proposition</h2>
            <p>We've generated a UVP based on your input. Please review and edit it as needed.</p>
            <div class="form-group">
                <textarea id="uvp-textarea" class="large-textarea">${uvp}</textarea>
            </div>
            <button id="next-step-2">Next: Generate Lexicon</button>
        `;

        document.getElementById('next-step-2').addEventListener('click', () => {
            state.uvp = document.getElementById('uvp-textarea').value;

            fetch(`${API_URL}/api/lexicon`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(state)
            })
            .then(response => response.json())
            .then(data => renderStep3(data.lexicon))
            .catch(error => console.error('Error fetching lexicon:', error));
        });
    }

    function renderStep3(lexicon) {
        const lexiconTableRows = lexicon.map((item, index) => `
            <tr>
                <td><input type="checkbox" id="lexicon-${index}" value="${item.word}" checked></td>
                <td><label for="lexicon-${index}">${item.word}</label></td>
                <td>${item.description}</td>
                <td>${item.relevance}</td>
            </tr>
        `).join('');

        app.innerHTML = `
            <h2>Step 3: Curate Your Lexicon</h2>
            <p>Select the words and phrases that best resonate with your brand identity.</p>
            <table class="lexicon-table">
                <thead>
                    <tr>
                        <th>Select</th>
                        <th>Word</th>
                        <th>Description</th>
                        <th>Relevance</th>
                    </tr>
                </thead>
                <tbody>
                    ${lexiconTableRows}
                </tbody>
            </table>
            <button id="next-step-3">Next: Generate Names</button>
        `;

        document.getElementById('next-step-3').addEventListener('click', () => {
            const selectedLexicon = [];
            lexicon.forEach((item, index) => {
                if (document.getElementById(`lexicon-${index}`).checked) {
                    selectedLexicon.push(item);
                }
            });
            state.lexicon = selectedLexicon;

            fetch(`${API_URL}/api/names`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(state)
            })
            .then(response => response.json())
            .then(data => renderStep4(data.names))
            .catch(error => console.error('Error fetching names:', error));
        });
    }

    function renderStep4(names) {
        const namesListHtml = names.map(nameInfo => `
            <div class="name-card">
                <h3>${nameInfo.name}</h3>
                <p><strong>.com Domain:</strong> <span class="${nameInfo.domainAvailable ? 'available' : 'unavailable'}">${nameInfo.domainAvailable ? 'Available' : 'Unavailable'}</span></p>
                <p><strong>Potential Competitors:</strong> ${nameInfo.competitors}</p>
            </div>
        `).join('');

        app.innerHTML = `
            <h2>Step 4: Choose Your Company Name</h2>
            <p>Here are some name suggestions based on your input. We've also checked for .com domain availability and potential competitors.</p>
            <div class="names-grid">
                ${namesListHtml}
            </div>
        `;
    }

    renderStep1();
});
