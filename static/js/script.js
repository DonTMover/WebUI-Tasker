// Обработка переключателя темы
const themeToggle = document.querySelector('.theme-toggle');
const setTheme = (isDark) => {
    document.body.classList.toggle('dark-mode', isDark); // Добавляем или убираем тёмную тему
    themeToggle.classList.toggle('dark', isDark); // Добавляем или убираем класс dark для переключателя
    const icon = themeToggle.querySelector('i');
    icon.classList.toggle('fa-moon', !isDark); // Луна для светлой темы
    icon.classList.toggle('fa-sun', isDark); // Солнце для тёмной темы
    localStorage.setItem('darkMode', isDark ? 'true' : 'false'); // Сохраняем состояние темы в localStorage
};

// Обработчик переключения темы
themeToggle.addEventListener('click', () => {
    const isDark = !document.body.classList.contains('dark-mode');
    setTheme(isDark);
});

// Восстановление состояния при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    const darkMode = localStorage.getItem('darkMode') === 'true';
    setTheme(darkMode);

    // Восстановление выбранного профиля и дня недели
    const savedProfile = localStorage.getItem('selectedProfile');
    const savedDay = localStorage.getItem('selectedDay');
    if (savedProfile) {
        document.querySelector('select[name="profile"]').value = savedProfile;
    }
    if (savedDay) {
        document.querySelector('select[name="day_of_week"]').value = savedDay;
    }
});

// Сохранение выбранного профиля и дня недели
document.querySelector('select[name="profile"]').addEventListener('change', (e) => {
    localStorage.setItem('selectedProfile', e.target.value); // Сохраняем выбранный профиль
});
document.querySelector('select[name="day_of_week"]').addEventListener('change', (e) => {
    localStorage.setItem('selectedDay', e.target.value); // Сохраняем выбранный день недели
});
