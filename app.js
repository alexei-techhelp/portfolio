let currentLang = 'ua'; // Default language

// Elements
const modalOverlay = document.getElementById('modal-overlay');
const modalTitle = document.getElementById('modal-title');
const modalTags = document.getElementById('modal-tags');
const modalBody = document.getElementById('modal-body');
const projectsGrid = document.getElementById('projects-grid');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Check local storage for language preference
    const savedLang = localStorage.getItem('portfolio_lang');
    if (savedLang) {
        currentLang = savedLang;
    }
    
    applyTranslations();
    renderProjects();
    setupIntersectionObserver();
});

// Language Switcher
function setLang(lang) {
    currentLang = lang;
    localStorage.setItem('portfolio_lang', lang);
    applyTranslations();
    renderProjects(); // Re-render projects to update text
    
    // Update active state on buttons
    document.getElementById('lang-en').className = lang === 'en' ? 'text-sm font-bold text-accent transition' : 'text-sm font-bold text-gray-500 hover:text-white transition';
    document.getElementById('lang-ua').className = lang === 'ua' ? 'text-sm font-bold text-accent transition' : 'text-sm font-bold text-gray-500 hover:text-white transition';
}

function applyTranslations() {
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[currentLang] && translations[currentLang][key]) {
            el.innerHTML = translations[currentLang][key];
        }
    });
}

// Render Projects
function renderProjects() {
    projectsGrid.innerHTML = '';
    
    projects.forEach((proj, index) => {
        // Create Card
        const card = document.createElement('div');
        card.className = `glass p-6 rounded-xl hover:-translate-y-2 transition-all duration-300 cursor-pointer border-t border-gray-700 hover:border-accent group fade-in`;
        card.style.animationDelay = `${index * 150}ms`;
        
        // Tags HTML
        const tagsHtml = proj.tags.map(tag => `<span class="text-xs font-semibold px-2 py-1 bg-gray-800 text-gray-300 rounded-md border border-gray-700">${tag}</span>`).join('');
        
        card.innerHTML = `
            <div class="h-48 -mx-6 -mt-6 mb-6 overflow-hidden rounded-t-xl relative border-b border-gray-800">
                <img src="${proj.image}" alt="${proj.title[currentLang]}" class="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-500">
                <div class="absolute inset-0 bg-gradient-to-t from-darker to-transparent opacity-80"></div>
            </div>
            <div class="flex flex-wrap gap-2 mb-4">
                ${tagsHtml}
            </div>
            <h3 class="text-xl font-bold mb-3 group-hover:text-accent transition-colors">${proj.title[currentLang]}</h3>
            <p class="text-gray-400 text-sm leading-relaxed mb-6">
                ${proj.summary[currentLang]}
            </p>
            <div class="flex items-center text-accent text-sm font-semibold opacity-0 group-hover:opacity-100 transition-opacity">
                <span>View Case Study</span>
                <i class="fa-solid fa-arrow-right ml-2 transform group-hover:translate-x-1 transition-transform"></i>
            </div>
        `;
        
        card.onclick = () => openModal(proj);
        projectsGrid.appendChild(card);
    });
    
    // Re-trigger observer for new elements
    setupIntersectionObserver();
}

// Modal Logic
function openModal(proj) {
    modalTitle.textContent = proj.title[currentLang];
    modalTags.innerHTML = proj.tags.map(tag => `<span class="text-xs font-semibold px-3 py-1 bg-accent/20 text-accent rounded-full border border-accent/30">${tag}</span>`).join('');
    modalBody.innerHTML = proj.content[currentLang];
    
    modalOverlay.classList.add('active');
    document.body.style.overflow = 'hidden'; // Prevent scrolling
}

function closeModal() {
    modalOverlay.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Close modal on outside click
modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) closeModal();
});

// Scroll Animations
function setupIntersectionObserver() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
}

// Navbar Scroll Effect
window.addEventListener('scroll', () => {
    const nav = document.getElementById('navbar');
    if (window.scrollY > 50) {
        nav.classList.add('shadow-lg');
        nav.classList.replace('border-gray-800', 'border-gray-700');
    } else {
        nav.classList.remove('shadow-lg');
        nav.classList.replace('border-gray-700', 'border-gray-800');
    }
});
