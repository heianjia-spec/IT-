<template>
  <el-container class="layout-container">
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
        <el-sub-menu index="settings-group" v-if="userStore.isAdmin">
          <template #title>
            <el-icon><User /></el-icon>
            <span>系统设置</span>
          </template>
          <el-menu-item index="/settings/users">用户管理</el-menu-item>
          <el-menu-item index="/settings/operation-logs">操作日志</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="layout-header">
        <div class="header-left">
          <el-icon class="collapse-btn" @click="isCollapse = !isCollapse" :size="20">
            <Fold v-if="!isCollapse" /><Expand v-else />
          </el-icon>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/dashboard' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item v-if="breadcrumb">{{ breadcrumb }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <span class="user-name">{{ userStore.user?.username }}</span>
          <el-dropdown @command="handleCommand">
            <el-avatar :size="32" style="cursor:pointer;margin-left:8px">{{ userStore.user?.username?.charAt(0)?.toUpperCase() }}</el-avatar>
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

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const isCollapse = ref(false)

const activeMenu = computed(() => {
  const path = route.path
  if (path.startsWith('/assets')) return path === '/assets/add' ? '/assets/add' : '/assets'
  if (path.startsWith('/basic-data')) return path
  if (path.startsWith('/notifications')) return path
  if (path.startsWith('/settings')) return path
  return path
})

const breadcrumb = computed(() => route.meta?.title || '')

const handleCommand = (cmd) => {
  if (cmd === 'logout') {
    userStore.logout()
    router.push('/login')
  }
}

// Fetch user on mount
userStore.fetchUser()
</script>

<style scoped>
.layout-container { height: 100vh; }
.layout-aside { background-color: #304156; overflow-y: auto; }
.logo { height: 60px; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 18px; font-weight: 600; border-bottom: 1px solid rgba(255,255,255,0.1); }
.logo-mini { font-size: 20px; }
.layout-header { display: flex; align-items: center; justify-content: space-between; background: #fff; box-shadow: 0 1px 4px rgba(0,0,0,0.08); padding: 0 20px; }
.header-left { display: flex; align-items: center; gap: 12px; }
.header-right { display: flex; align-items: center; }
.collapse-btn { cursor: pointer; }
.user-name { font-size: 14px; color: #606266; }
.layout-main { background: #f5f7fa; padding: 20px; min-height: calc(100vh - 60px); }
</style>
