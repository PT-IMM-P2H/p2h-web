# ✅ Responsive Testing Checklist

Gunakan checklist ini untuk memastikan semua halaman responsive dengan baik.

---

## 🔧 Cara Test

### 1. Browser DevTools (Chrome/Edge)
1. Tekan `F12` untuk buka DevTools
2. Tekan `Ctrl+Shift+M` untuk toggle device toolbar
3. Pilih preset devices atau custom size

### 2. Test di Multiple Devices
- iPhone SE (375px × 667px)
- iPhone 12 Pro (390px × 844px)
- iPad (768px × 1024px)
- iPad Pro (1024px × 1366px)
- Desktop (1920px × 1080px)

### 3. Test Orientasi
- Portrait (vertical)
- Landscape (horizontal)

---

## 📱 Mobile Testing (375px - 639px)

### Sidebar/Navigation
- [ ] Sidebar hidden by default
- [ ] Hamburger menu button visible di header
- [ ] Klik hamburger menu → sidebar slide in dari kiri
- [ ] Overlay hitam muncul di belakang sidebar
- [ ] Klik overlay → sidebar close
- [ ] Klik X button → sidebar close
- [ ] Klik menu item → navigate & sidebar auto close
- [ ] Language selector berfungsi
- [ ] Logout button berfungsi

### Header
**Admin Header:**
- [ ] Hamburger button (kiri) visible
- [ ] Title truncate jika terlalu panjang
- [ ] Date visible (bisa hide di mobile kecil)
- [ ] User name hidden di mobile
- [ ] Avatar button visible dan clickable

**User Header:**
- [ ] Logo + title visible
- [ ] Desktop nav links hidden
- [ ] Hamburger button visible
- [ ] Mobile menu slide down smooth
- [ ] All nav links dalam mobile menu berfungsi
- [ ] Logout button dalam mobile menu berfungsi

### Dashboard
- [ ] 6 cards dalam 2 kolom (grid-cols-2)
- [ ] Cards clickable dan show detail
- [ ] Text dalam card readable (tidak terpotong)
- [ ] Icons tidak terlalu besar
- [ ] Filter section full width
- [ ] Date picker berfungsi (tidak zoom di iOS)
- [ ] Dropdown tipe kendaraan berfungsi
- [ ] Charts responsive dan readable
- [ ] Pie charts tidak distort

### Tables
- [ ] Table scroll horizontal smooth
- [ ] Minimal columns visible (hide non-essential)
- [ ] Text dalam cell readable (text-xs atau text-sm)
- [ ] Checkbox cukup besar untuk tap (min 44px)
- [ ] Row clickable/selectable
- [ ] Pagination buttons cukup besar
- [ ] Search box full width
- [ ] Filter buttons stack vertical atau wrap

### Forms
- [ ] All inputs full width
- [ ] Input font-size >= 16px (no zoom di iOS)
- [ ] Labels clear dan readable
- [ ] Buttons full width atau stack vertical
- [ ] Date/time picker berfungsi tanpa zoom
- [ ] Dropdown/select full width
- [ ] Error messages visible
- [ ] Submit/cancel buttons jelas

### Modals
- [ ] Modal full width (margin minimal)
- [ ] Modal max-height 90vh dengan scroll
- [ ] Close button (X) cukup besar untuk tap
- [ ] Title tidak terpotong
- [ ] Content scrollable jika panjang
- [ ] Footer buttons stack atau full width
- [ ] Overlay click to close berfungsi

### Cards/Statistik
- [ ] Cards dalam 2 kolom
- [ ] Icon + value + label semua visible
- [ ] Hover effect berfungsi (tap di mobile)
- [ ] Click event berfungsi
- [ ] Loading state visible

---

## 📱 Tablet Testing (640px - 1023px)

### Layout
- [ ] Sidebar masih hamburger menu (< 1024px)
- [ ] Dashboard cards dalam 3 kolom
- [ ] Tables show more columns
- [ ] Modals medium size (tidak full screen)
- [ ] Forms dalam grid 2 kolom

### Navigation
- [ ] Hamburger menu berfungsi
- [ ] Sidebar slide smooth
- [ ] Menu items clickable

### Components
- [ ] All components scale appropriately
- [ ] Text size comfortable untuk tablet
- [ ] Touch targets masih >= 44px

---

## 💻 Desktop Testing (1024px+)

### Sidebar
- [ ] Sidebar always visible (fixed)
- [ ] No hamburger menu di header
- [ ] Sidebar width 248px (w-62)
- [ ] Menu expand/collapse smooth
- [ ] Nested menu items visible

### Header
- [ ] Full title + date visible
- [ ] User name + role visible
- [ ] Avatar button di kanan

### Dashboard
- [ ] 6 cards dalam 1 baris (grid-cols-6)
- [ ] All components full size
- [ ] Charts readable dan detail
- [ ] Filter section dalam row

### Tables
- [ ] All columns visible
- [ ] No horizontal scroll (kecuali banyak kolom)
- [ ] Hover effects berfungsi
- [ ] Sorting berfungsi

### Modals
- [ ] Modal center screen
- [ ] Appropriate size (small/medium/large)
- [ ] Not too wide, not too narrow
- [ ] Overlay blur/darken background

---

## 🎨 Visual Testing

### Typography
- [ ] All text readable
- [ ] Font sizes appropriate per breakpoint
- [ ] Line heights comfortable
- [ ] No text overflow/cut off

### Spacing
- [ ] Padding/margin consistent
- [ ] No elements touching edges
- [ ] Gaps between elements appropriate
- [ ] White space balanced

### Colors
- [ ] Contrast ratio accessible (WCAG AA)
- [ ] Hover states visible
- [ ] Active states clear
- [ ] Disabled states obvious

### Icons
- [ ] Icons size appropriate
- [ ] Icons align with text
- [ ] Icons visible dan recognizable
- [ ] SVG icons crisp (not pixelated)

---

## 🔄 Interaction Testing

### Touch/Click
- [ ] All buttons tappable (min 44x44px)
- [ ] Links clickable
- [ ] Checkboxes/radios easy to select
- [ ] Dropdowns open smooth
- [ ] Date pickers functional

### Scrolling
- [ ] Page scroll smooth
- [ ] Table horizontal scroll smooth
- [ ] Modal content scroll smooth
- [ ] No unexpected scroll behavior
- [ ] Scrollbar visible saat needed

### Animations
- [ ] Sidebar slide smooth
- [ ] Modal open/close smooth
- [ ] Dropdown expand/collapse smooth
- [ ] Hover effects tidak jittery
- [ ] Loading spinners smooth

---

## ⚡ Performance Testing

### Load Time
- [ ] Initial load < 3 detik
- [ ] Components render cepat
- [ ] Images load progressively
- [ ] No layout shift saat load

### Responsiveness
- [ ] UI responds cepat ke input
- [ ] No lag saat scroll
- [ ] No lag saat toggle sidebar
- [ ] Smooth di device lama

---

## ♿ Accessibility Testing

### Keyboard Navigation
- [ ] Tab order logical
- [ ] Focus states visible
- [ ] Enter/Space activate buttons
- [ ] Esc close modals
- [ ] Arrow keys dalam dropdown

### Screen Reader
- [ ] Alt text untuk images
- [ ] ARIA labels untuk icons
- [ ] Form labels associated
- [ ] Error messages announced

### Color Contrast
- [ ] Text readable untuk color blind
- [ ] Links distinguishable
- [ ] Buttons clear

---

## 🌐 Browser Testing

Test di semua major browsers:

### Chrome/Edge
- [ ] Mobile view
- [ ] Tablet view
- [ ] Desktop view

### Firefox
- [ ] Mobile view
- [ ] Tablet view
- [ ] Desktop view

### Safari (iOS)
- [ ] iPhone view
- [ ] iPad view
- [ ] No zoom on input focus
- [ ] Safari menu tidak overlap content

### Samsung Internet
- [ ] Mobile view
- [ ] Tablet view

---

## 🐛 Common Issues to Check

### Mobile
- [ ] ❌ Horizontal scroll (bad)
- [ ] ❌ Tiny text (< 12px)
- [ ] ❌ Small tap targets (< 44px)
- [ ] ❌ Zoom on input focus (iOS)
- [ ] ❌ Fixed elements overlap
- [ ] ❌ Modals not full width
- [ ] ❌ Images overflow container

### All Devices
- [ ] ❌ Layout breaks at certain width
- [ ] ❌ Text overflow ellipsis not working
- [ ] ❌ Tables tidak scrollable
- [ ] ❌ Buttons overlapping
- [ ] ❌ z-index issues (modals, dropdowns)

---

## ✅ Final Checklist

Sebelum deploy ke production:

- [ ] Test semua halaman di mobile (375px)
- [ ] Test semua halaman di tablet (768px)
- [ ] Test semua halaman di desktop (1024px+)
- [ ] Test di real iPhone
- [ ] Test di real Android
- [ ] Test di real iPad
- [ ] Test landscape mode
- [ ] Test slow 3G network
- [ ] Test dengan screen reader
- [ ] Test keyboard navigation
- [ ] Lighthouse score > 90
- [ ] No console errors
- [ ] No visual bugs
- [ ] All features berfungsi

---

## 📊 Lighthouse Audit

Jalankan Lighthouse di Chrome DevTools:

**Target Scores:**
- Performance: > 90
- Accessibility: > 95
- Best Practices: > 95
- SEO: > 90

**Cara:**
1. Buka Chrome DevTools (F12)
2. Tab "Lighthouse"
3. Select "Mobile" atau "Desktop"
4. Click "Analyze page load"
5. Review dan fix issues

---

## 📝 Bug Report Template

Jika menemukan bug:

```
**Device:** iPhone 12 Pro
**Browser:** Safari 15
**Screen Size:** 390 x 844
**Page:** Dashboard
**Issue:** Sidebar tidak close saat klik overlay
**Steps to Reproduce:**
1. Buka dashboard di mobile
2. Klik hamburger menu
3. Sidebar muncul
4. Klik area gelap (overlay)
**Expected:** Sidebar close
**Actual:** Sidebar tetap open
**Screenshot:** [attach]
```

---

**Happy Testing! 🎉**

Jika menemukan issue, laporkan dengan detail menggunakan template di atas.
