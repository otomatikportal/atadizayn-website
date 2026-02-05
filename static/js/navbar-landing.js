(function() {
  const navbar = document.getElementById('site-navbar');
  if (!navbar) return;

  const isLanding = document.body.dataset.landingNav === '1';
  if (!isLanding) return;

  const hideNav = () => { navbar.style.transform = 'translateY(-110%)'; };
  const showNav = () => { navbar.style.transform = 'translateY(0)'; };

  const onScroll = () => {
    if (window.scrollY > 100) {
      showNav();
    } else {
      hideNav();
    }
  };

  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
})();
