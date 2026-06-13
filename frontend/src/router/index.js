import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/LoginView.vue'),
    meta: { public: true },
  },
  {
    path: '/',
    component: () => import('../components/layout/AppLayout.vue'),
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', name: 'Dashboard', component: () => import('../views/dashboard/DashboardView.vue') },
      { path: 'assets', name: 'AssetList', component: () => import('../views/assets/AssetListView.vue') },
      { path: 'assets/add', name: 'AssetAdd', component: () => import('../views/assets/AssetFormView.vue') },
      { path: 'assets/:id', name: 'AssetDetail', component: () => import('../views/assets/AssetDetailView.vue') },
      { path: 'assets/:id/edit', name: 'AssetEdit', component: () => import('../views/assets/AssetFormView.vue') },
      { path: 'basic-data/categories', name: 'Categories', component: () => import('../views/baseData/CategoryView.vue') },
      { path: 'basic-data/departments', name: 'Departments', component: () => import('../views/baseData/DepartmentView.vue') },
      { path: 'basic-data/locations', name: 'Locations', component: () => import('../views/baseData/LocationView.vue') },
      { path: 'basic-data/suppliers', name: 'Suppliers', component: () => import('../views/baseData/SupplierView.vue') },
      { path: 'notifications/rules', name: 'AlertRules', component: () => import('../views/alerts/AlertRuleView.vue') },
      { path: 'notifications/logs', name: 'AlertLogs', component: () => import('../views/alerts/AlertLogView.vue') },
      { path: 'notifications/email-config', name: 'EmailConfig', component: () => import('../views/alerts/EmailConfigView.vue') },
    { path: 'notifications/email-template', name: 'EmailTemplate', component: () => import('../views/alerts/EmailTemplateView.vue') },
      { path: 'settings/users', name: 'UserManagement', component: () => import('../views/settings/UserManagement.vue') },
    { path: 'settings/operation-logs', name: 'OperationLogs', component: () => import('../views/assets/OperationLogView.vue') },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  if (to.meta.public) {
    next()
  } else if (!token) {
    next('/login')
  } else {
    next()
  }
})

export default router
