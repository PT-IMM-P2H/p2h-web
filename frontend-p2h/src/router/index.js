import { createRouter, createWebHistory } from "vue-router";
import Main from '../views/main.vue'
import LoginPage from '../components/login-page.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/login',
            name: 'login',
            component: LoginPage
        },
        {
            path: '/',
            name: 'main',
            component: Main
        },
        {
            path: '/monitor-kendaraan',
            name: 'monitor-kendaraan',
            component: () => import('../components/viewer/monitor.vue')
        },
        {
            path: '/form-p2h',
            name: 'form-p2h',
            component: () => import('../components/user/p2h_form.vue')
        },
        {
            path: '/profile-user',
            name: 'profile-user',
            component: () => import('../components/user/profile.vue')
        },
        {
            path: '/riwayat-user',
            name: 'riwayat-user',
            component: () => import('../components/user/riwayat-user.vue')
        },
        {
            path: '/dashboard',
            name: 'dashboard',
            component: () => import('../components/admin/dashboard.vue')
        },
        {
            path:'/hasil-form',
            name:'hasil-form',
            component: () => import('../components/user/hasil_form.vue')
        },
        {
            path: '/data-monitor-pt',
            name: 'data-monitor-pt',
            component: () => import('../components/admin/data_monitor/data-monitor-pt.vue')
        },
        {
            path: '/data-monitor-travel',
            name: 'data-monitor-travel',
            component: () => import('../components/admin/data_monitor/data-monitor-travel.vue')
        },
        {
            path: '/data-pengguna-pt',
            name: 'data-pengguna-pt',
            component: () => import('../components/admin/data_pengguna/data-pengguna-pt.vue')
        },
        {
            path: '/data-pengguna-travel',
            name: 'data-pengguna-travel',
            component: () => import('../components/admin/data_pengguna/data-pengguna-travel.vue')
        },
        {
            path: '/kelola-pertanyaan',
            name: 'kelola-pertanyaan',
            component: () => import('../components/admin/kelola-pertanyaan.vue')
        },
        {
            path: '/data-perusahaan',
            name: 'data-perusahaan',
            component: () => import('../components/admin/master_data/data-perusahaan.vue')
        },
        {
            path: '/data-departemen',
            name: 'data-departemen',
            component: () => import('../components/admin/master_data/data-departemen.vue')
        },
        {
            path: '/data-posisi',
            name: 'data-posisi',
            component: () => import('../components/admin/master_data/data-posisi.vue')
        },
        {
            path: '/data-status',
            name: 'data-status',
            component: () => import('../components/admin/master_data/data-status.vue')
        },
        {
            path: '/unit-kendaraan-pt',
            name: 'unit-kendaraan-pt',
            component: () => import('../components/admin/unit-kendaraan/unit-pt.vue')
        },
        {
            path: '/unit-kendaraan-travel',
            name: 'unit-kendaraan-travel',
            component: () => import('../components/admin/unit-kendaraan/unit-travel.vue')
        },
        {
            path: '/profil-admin',
            name: 'profil-admin',
            component: () => import('../components/admin/profil-admin.vue')
        },
    ],
    scrollBehavior(to, from, savedPosition) {
        return { top: 0 }
    }
})

// Navigation Guard untuk Role-Based Authorization
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('access_token');
    const userRole = localStorage.getItem('user_role');
    
    // Route yang tidak perlu autentikasi
    const publicRoutes = ['login', 'main', 'monitor-kendaraan'];
    
    // Routes khusus admin/superadmin
    const adminRoutes = [
        'dashboard',
        'data-monitor-pt',
        'data-monitor-travel',
        'data-pengguna-pt',
        'data-pengguna-travel',
        'kelola-pertanyaan',
        'data-perusahaan',
        'data-departemen',
        'data-posisi',
        'data-status',
        'unit-kendaraan-pt',
        'unit-kendaraan-travel',
        'profil-admin'
    ];
    
    // Routes untuk user biasa
    const userRoutes = [
        'form-p2h',
        'profile-user',
        'riwayat-user',
        'hasil-form'
    ];
    
    // Jika belum login dan mengakses route yang butuh auth
    if (!token && !publicRoutes.includes(to.name)) {
        return next({ name: 'login' });
    }
    
    // Jika sudah login
    if (token && userRole) {
        // Viewer hanya boleh akses monitor
        if (userRole === 'viewer') {
            if (!publicRoutes.includes(to.name)) {
                return next({ name: 'monitor-kendaraan' });
            }
            return next(); // Important: allow navigation
        }
        
        // User biasa tidak boleh akses admin routes
        if (userRole === 'user') {
            if (adminRoutes.includes(to.name)) {
                return next({ name: 'form-p2h' });
            }
            // Redirect dari login ke form-p2h
            if (to.name === 'login' || to.name === 'main') {
                return next({ name: 'form-p2h' });
            }
            return next(); // Important: allow navigation
        }
        
        // Admin/Superadmin redirect dari login ke dashboard
        if (userRole === 'admin' || userRole === 'superadmin') {
            if (to.name === 'login' || to.name === 'main') {
                return next({ name: 'dashboard' });
            }
            return next(); // Important: allow navigation to other routes
        }
    }
    
    next();
});

export default router;
