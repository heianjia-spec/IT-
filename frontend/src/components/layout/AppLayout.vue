<template>
  <el-container class="layout-container">
    <!-- 左侧菜单栏 -->
    <el-aside :width="isCollapse ? '64px' : '220px'" class="layout-aside">
      <div class="logo">
        <span v-if="!isCollapse">IT资产管理系统</span>
        <span v-else class="logo-mini">IT</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <el-menu-item index="/dashboard">
          <el-icon><DataAnalysis /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-sub-menu index="assets-group">
          <template #title>
            <el-icon><Monitor /></el-icon>
            <span>资产管理</span>
          </template>
          <el-menu-item index="/assets">资产列表</el-menu-item>
          <el-menu-item index="/assets/add">新增资产</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="base-data-group">
          <template #title>
            <el-icon><Setting /></el-icon>
            <span>基础数据</span>
          </template>
          <el-menu-item index="/basic-data/categories">资产分类</el-menu-item>
          <el-menu-item index="/basic-data/departments">部门管理</el-menu-item>
          <el-menu-item index="/basic-data/locations">位置管理</el-menu-item>
          <el-menu-item index="/basic-data/suppliers">供应商管理</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="notifications-group" v-if="userStore.canWrite">
          <template #title>
            <el-icon><Bell /></el-icon>
            <span>通知与告警</span>
          </template>
          <el-menu-item index="/notifications/rules">告警规则</el-menu-item>
          <el-menu-item index="/notifications/logs">告警日志</el-menu-item>
          <el-menu-item index="/notifications/email-config">邮件配置</el-menu-item>
          <el-menu-item index="/notifications/email-template">邮件模板</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="settings-group" v-if="userStore.canWrite">
          <template #title>
            <el-icon><User /></el-icon>
            <span>系统设置</span>
          </template>
          <el-menu-item index="/settings/users" v-if="userStore.isAdmin">用户管理</el-menu-item>
          <el-menu-item index="/settings/form-templates">表单模板</el-menu-item>
          <el-menu-item index="/settings/operation-logs">操作日志</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>

    <el-container class="right-container">
      <!-- 顶部 Header -->
      <el-header class="layout-header">
        <div class="header-left">
          <el-icon class="collapse-btn" @click="isCollapse = !isCollapse" :size="20">
            <Fold v-if="!isCollapse" /><Expand v-else />
          </el-icon>
          <span class="user-name">{{ userStore.user?.username }}</span>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <el-avatar :size="32" style="cursor:pointer">{{ userStore.user?.username?.charAt(0)?.toUpperCase() }}</el-avatar>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                <el-dropdown-item command="password">修改密码</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 面包屑导航条 -->
      <div class="breadcrumb-bar">
        <el-breadcrumb separator=">">
          <el-breadcrumb-item :to="{ path: '/dashboard' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item
            v-for="(item, idx) in breadcrumbItems"
            :key="idx"
            :to="item.path ? { path: item.path } : undefined"
          >
            {{ item.label }}
          </el-breadcrumb-item>
        </el-breadcrumb>
      </div>

      <!-- 主内容区 -->
      <el-main class="layout-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../../store/user'
import { DataAnalysis, Monitor, Setting, Bell, User, Fold, Expand } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const isCollapse = ref(false)

const activeMenu = computed(() => {
  const path = route.path
  if (path.startsWith('/assets')) return path === '/assets/add' || path === '/assets' ? path : '/assets'
  if (path.startsWith('/basic-data')) return path
  if (path.startsWith('/notifications')) return path
  if (path.startsWith('/settings')) return path
  return path
})

// 面包屑：根据路由路径动态生成
const breadcrumbItems = computed(() => {
  const path = route.path
  const items = []

  // 资产管理
  if (path.startsWith('/assets')) {
    items.push({ label: '资产管理', path: '/assets' })
    if (path === '/assets') {
      items.push({ label: '资产列表', path: '' })
    } else if (path === '/assets/add') {
      items.push({ label: '新增资产', path: '' })
    } else if (path.match(/^\/assets\/\d+\/edit$/)) {
      items.push({ label: '编辑资产', path: '' })
    } else if (path.match(/^\/assets\/\d+$/)) {
      items.push({ label: '资产详情', path: '' })
    }
  }
  // 基础数据
  else if (path.startsWith('/basic-data')) {
    items.push({ label: '基础数据', path: '/basic-data/categories' })
    const map = {
      '/basic-data/categories': '资产分类',
      '/basic-data/departments': '部门管理',
      '/basic-data/locations': '位置管理',
      '/basic-data/suppliers': '供应商管理',
    }
    items.push({ label: map[path] || '', path: '' })
  }
  // 通知与告警
  else if (path.startsWith('/notifications')) {
    items.push({ label: '通知与告警', path: '/notifications/rules' })
    const map = {
      '/notifications/rules': '告警规则',
      '/notifications/logs': '告警日志',
      '/notifications/email-config': '邮件配置',
      '/notifications/email-template': '邮件模板',
    }
    items.push({ label: map[path] || '', path: '' })
  }
  // 系统设置
  else if (path.startsWith('/settings')) {
    items.push({ label: '系统设置', path: '/settings/form-templates' })
    const map = {
      '/settings/users': '用户管理',
      '/settings/form-templates': '表单模板',
      '/settings/operation-logs': '操作日志',
    }
    items.push({ label: map[path] || '', path: '' })
  }

  return items
})

const handleCommand = (cmd) => {
  if (cmd === 'logout') {
    userStore.logout()
    router.push('/login')
  }
}

userStore.fetchUser()
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

/* ========== 左侧菜单栏 ========== */
.layout-aside {
  background-color: #304156;
  overflow-y: auto;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-mini {
  font-size: 20px;
}

/* ========== 右侧容器 ========== */
.right-container {
  flex-direction: column;
}

/* ========== 顶部 Header ========== */
.layout-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  padding: 0 20px;
  height: 50px;
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-right {
  display: flex;
  align-items: center;
}

.collapse-btn {
  cursor: pointer;
}

.user-name {
  font-size: 14px;
  color: #606266;
}

/* ========== 面包屑导航条 ========== */
.breadcrumb-bar {
  display: flex;
  align-items: center;
  height: 36px;
  padding: 0 20px;
  background-color: #f5f7fa;
  border-bottom: 1px solid #e4e7ed;
  flex-shrink: 0;
}

:deep(.el-breadcrumb) {
  font-size: 13px;
}

:deep(.el-breadcrumb__inner) {
  color: #606266;
  transition: color 0.2s;
}

:deep(.el-breadcrumb__inner.is-link:hover) {
  color: #409EFF;
}

/* 最后一个节点：当前页，加粗不可点击 */
:deep(.el-breadcrumb__item:last-child .el-breadcrumb__inner) {
  font-weight: 600;
  color: #303133;
}

/* ========== 主内容区 ========== */
.layout-main {
  flex: 1;
  background: #f5f7fa;
  padding: 20px;
  overflow-y: auto;
}
</style>
