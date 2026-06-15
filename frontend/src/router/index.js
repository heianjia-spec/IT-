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
      { path: 'dashboard', name: 'Dashboard', component: () => import('../views/dashboard/DashboardView.vue'), meta: { title: '仪表盘' } },
      { path: 'assets', name: 'AssetList', component: () => import('../views/assets/AssetListView.vue'), meta: { title: '资产列表' } },
      { path: 'assets/add', name: 'AssetAdd', component: () => import('../views/assets/AssetFormView.vue'), meta: { title: '新增资产' } },
      { path: 'assets/:id', name: 'AssetDetail', component: () => import('../views/assets/AssetDetailView.vue'), meta: { title: '资产详情' } },
      { path: 'assets/:id/edit', name: 'AssetEdit', component: () => import('../views/assets/AssetFormView.vue'), meta: { title: '编辑资产' } },
      { path: 'basic-data/categories', name: 'Categories', component: () => import('../views/baseData/CategoryView.vue'), meta: { title: '资产分类' } },
      { path: 'basic-data/departments', name: 'Departments', component: () => import('../views/baseData/DepartmentView.vue'), meta: { title: '部门管理' } },
      { path: 'basic-data/locations', name: 'Locations', component: () => import('../views/baseData/LocationView.vue'), meta: { title: '位置管理' } },
      { path: 'basic-data/suppliers', name: 'Suppliers', component: () => import('../views/baseData/SupplierView.vue'), meta: { title: '供应商管理' } },
      { path: 'notifications/rules', name: 'AlertRules', component: () => import('../views/alerts/AlertRuleView.vue'), meta: { title: '告警规则' } },
      { path: 'notifications/logs', name: 'AlertLogs', component: () => import('../views/alerts/AlertLogView.vue'), meta: { title: '告警日志' } },
      { path: 'notifications/email-config', name: 'EmailConfig', component: () => import('../views/alerts/EmailConfigView.vue'), meta: { title: '邮件配置' } },
    { path: 'notifications/email-template', name: 'EmailTemplate', component: () => import('../views/alerts/EmailTemplateView.vue'), meta: { title: '邮件模板' } },
      { path: 'settings/users', name: 'UserManagement', component: () => import('../views/settings/UserManagement.vue'), meta: { title: '用户管理' } },
    { path: 'settings/operation-logs', name: 'OperationLogs', component: () => import('../views/assets/OperationLogView.vue'), meta: { title: '操作日志' } },
      { path: 'settings/form-templates', name: 'FormTemplates', component: () => import('../views/settings/TemplateEditorView.vue'), meta: { title: '表单模板' } },
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
