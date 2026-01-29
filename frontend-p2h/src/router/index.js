import { createRouter, createWebHistory } from "vue-router";
import Main from '../views/main.vue'
import LoginPage from '../components/login-page.vue'
import { STORAGE_KEYS } from '../constants'

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
            meta: { requiresAuth: false, public: true }
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

// Helper function to check if token is expired
function isTokenExpired(token) {
    if (!token) return true;
    
    try {
        // Decode JWT token (simple base64 decode of payload)
        const payload = JSON.parse(atob(token.split('.')[1]));
        const exp = payload.exp;
        
        if (!exp) return false; // No expiration set
        
        // Check if token expired (exp is in seconds, Date.now() is in milliseconds)
        const now = Math.floor(Date.now() / 1000);
        return now >= exp;
    } catch (e) {
        console.error('Error checking token expiration:', e);
        return true; // Treat invalid tokens as expired
    }
}

// Navigation Guard untuk Role-Based Authorization
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
    const userRole = localStorage.getItem('user_role');

    // Check if token is expired
    if (token && isTokenExpired(token)) {
        console.log('⚠️ Token expired, logging out...');
        localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
        localStorage.removeItem('user_role');
        localStorage.removeItem('user_data');
        
        // If trying to access protected route, redirect to login
        const publicRoutes = ['login', 'main', 'monitoring-kendaraan'];
        if (!publicRoutes.includes(to.name)) {
            alert('Sesi Anda telah berakhir. Silakan login kembali.');
            return next({ name: 'login' });
        }
    }
    
    console.log('🔍 Navigation Guard:', {
        from: from.name,
        to: to.name,
        hasToken: !!token,
        userRole: userRole
    });
    
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
        console.log('✅ User authenticated with role:', userRole);
        
        // Viewer hanya boleh akses monitor
        if (userRole === 'viewer') {
            if (!publicRoutes.includes(to.name)) {
                console.log('🚫 Viewer blocked from:', to.name);
                return next({ name: 'monitor-kendaraan' });
            }
            console.log('✅ Viewer allowed to:', to.name);
            return next();
        }
        
        // User biasa tidak boleh akses admin routes
        if (userRole === 'user') {
            if (adminRoutes.includes(to.name)) {
                console.log('🚫 User blocked from admin route:', to.name);
                return next({ name: 'form-p2h' });
            }
            if (to.name === 'login' || to.name === 'main') {
                console.log('🔄 User redirected from', to.name, 'to form-p2h');
                return next({ name: 'form-p2h' });
            }
            console.log('✅ User allowed to:', to.name);
            return next();
        }
        
        // Admin/Superadmin redirect dari login ke dashboard
        if (userRole === 'admin' || userRole === 'superadmin') {
            if (to.name === 'login' || to.name === 'main') {
                console.log('🔄 Admin/Superadmin redirected from', to.name, 'to dashboard');
                return next({ name: 'dashboard' });
            }
            console.log('✅ Admin/Superadmin allowed to:', to.name);
            return next();
        }
    }
    
    console.log('➡️ Fallback next() called');
    next();
});

export default router;
