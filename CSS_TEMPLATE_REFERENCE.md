# 🎨 CSS & Template Enhancement Reference

## CSS Animations Added

```css
/* Entrance Animations */
@keyframes slide-in-left { }    /* Slides in from left with fade */
@keyframes slide-in-right { }   /* Slides in from right with fade */
@keyframes bounce-in { }        /* Bounces in with scale effect */

/* Effect Animations */
@keyframes float-down { }       /* Floating up and down motion */
@keyframes glow-pulse { }       /* Pulsing glow effect */
@keyframes shimmer { }          /* Shimmer/shine effect */
@keyframes neon-glow { }        /* Text glow animation */
@keyframes pulse-scale { }      /* Pulsing scale animation */
```

## New CSS Classes

### Typography
- `.hero-title` - Large animated page titles
- `.hero-description` - Subtitle styling with animations
- `.gradient-text` - Text with gradient colors
- `.text-gold`, `.text-cyan`, `.text-purple`, `.text-pink` - Color utilities

### Cards & Containers
- `.neon-card` - Base card styling with hover effects
- `.neon-card-cyan-border` - Cyan-bordered cards
- `.neon-card-lime-border` - Gold-bordered cards
- `.neon-card-purple-border` - Purple-bordered cards
- `.neon-card-pink-border` - Pink-bordered cards
- `.stat-box` - Statistics display boxes
- `.rounded-royal` - Royal border-radius styling

### Interactive Elements
- `.btn-royal` - Primary gradient buttons with ripple
- `.btn-outline-custom` - Outlined custom buttons
- `.challenge-card` - Challenge card styling with animations
- `.challenge-status-badge` - Completion status badge
- `.difficulty-indicator` - Difficulty level styling
- `.difficulty-beginner`, `.difficulty-intermediate`, `.difficulty-advanced` - Difficulty colors

### Badges & Status
- `.badge` - Base badge styling with animations
- `.badge-success` - Green success badges
- `.badge-warning` - Yellow warning badges
- `.badge-danger` - Red danger badges
- `.badge-info` - Blue info badges

### Progress
- `.progress` - Enhanced progress bar container
- `.progress-bar` - Animated gradient progress bar

### Forms
- `.form-control` - Enhanced input styling
- `.form-control:focus` - Focus state with glow

### Utility Classes
- `.glow-gold`, `.glow-cyan` - Text glow effects
- `.shadow-lg-custom` - Large custom shadows
- `.animation-*` - Various animation utilities

## Template Enhancements

### Homepage (core/home.html)
```html
<!-- Enhanced with: -->
- Gradient hero sections
- Learning platform highlights (4 cards)
- Better quick access layout
- Improved activity display
- Status indicators
- Animated entrances
```

### Dashboard (learning/dashboard.html)
```html
<!-- Enhanced with: -->
- Large animated statistics
- Color-coded difficulty boxes
- Better hero section
- Prominent stat display
- Enhanced buttons with icons
- Improved navigation cards
```

### Challenges (learning/challenges.html)
```html
<!-- Enhanced with: -->
- Animated challenge cards
- Completion status badges
- Difficulty indicators
- Progress bars for hints
- Attempt counters
- Better filter UI
- Responsive grid layout
- Bounce-in animations
```

## Color Palette Reference

```css
--neon-cyan: #C9A961      /* Gold/Cyan */
--neon-pink: #E8D5C4      /* Cream/Pink */
--neon-lime: #D4AF37      /* Deep Gold */
--neon-purple: #6B4C9A    /* Royal Purple */
--neon-blue: #3D5A80      /* Navy Blue */
--text-primary: #f5f5f0   /* Light Text */
--text-secondary: #c9c9c0 /* Gray Text */
```

## Animation Timing

- Standard transitions: `0.3s ease`
- Page animations: `0.8s ease-out`
- Hover effects: `0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)`
- Staggered animations: `0.1s - 0.4s delays`

## Responsive Breakpoints

- Large screens (lg): `≥992px`
- Medium screens (md): `≥768px`
- Small screens (sm): `<768px`

## Border Styles

- Card borders: `2px solid`
- Accent borders: `3px solid` (hero sections)
- Light borders: `1px solid rgba(...)`

## Shadow Styles

- Card hover: `0 12px 40px rgba(212, 175, 55, 0.25)`
- Small shadow: `0 0 12px rgba(212, 175, 55, 0.2)`
- Large shadow: `0 20px 50px rgba(212, 175, 55, 0.2)`

## Hover Effects

All interactive elements now have:
- Smooth color transitions
- Transform animations (lift, scale)
- Enhanced box-shadows
- Text-shadow effects
- Background transitions

## Backdrop Effects

- `.neon-card::before` - Shimmer overlay on hover
- `.progress-bar::after` - Shine animation
- `backdrop-filter: blur(5px-10px)` - Frost glass effect

## Z-index Hierarchy

- Base: `z-index: 1`
- Overlays: `z-index: 10`
- Modals/Dropdowns: Higher values

## Font Families

- Display: `'Orbitron', monospace` (titles)
- Body: `'Share Tech Mono', monospace` (content)
- Bootstrap: System fonts (fallback)

## Implementation Notes

### For Developers
1. Use CSS variables for colors
2. Apply animation classes to elements
3. Use responsive utilities for mobile
4. Follow the grid system for layouts
5. Use semantic HTML structure

### Performance Tips
1. Animations use `transform` and `opacity` (GPU accelerated)
2. Transitions use `ease` for smooth motion
3. Animations are optional (no critical functionality)
4. Mobile animations may be reduced for performance

### Accessibility
1. High contrast colors (meeting WCAG AA)
2. Semantic HTML for screen readers
3. Color not sole indicator of status
4. Clear focus states on interactive elements
5. Readable font sizes

## Testing Recommendations

- Test animations in Chrome, Firefox, Safari
- Verify mobile responsiveness
- Check color contrast with accessibility tools
- Test keyboard navigation
- Verify loading performance

---

**Last Updated**: April 13, 2026  
**CSS Version**: 2.1  
**Status**: Complete ✅
