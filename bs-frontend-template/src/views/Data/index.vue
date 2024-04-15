<template>
  <div class="data-main">
    <el-tabs tab-position="top" class="demo-tabs" type="card">
      <el-tab-pane label="读者分类借阅率">
        <iframe :src="getSrc('/admin/library/duzhefenlei/')"></iframe>
      </el-tab-pane>
      <el-tab-pane label="图书借阅排行">
        <iframe :src="getSrc('/admin/library/tushu/')"></iframe>
      </el-tab-pane>
      <el-tab-pane label="分类借阅统计">
        <iframe :src="getSrc('/admin/library/tushufenlei/')"></iframe>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
const index = import.meta.env.VITE_API_BASE_URL.replace("/api", "");
const getSrc = (e) => {
  return `${index}${e}`;
};
</script>

<style lang="postcss">
.data-main {
  height: 1000px;
  .el-tabs {
    height: 100%;
    .el-tabs__content {
      padding: 0px !important;
      height: calc(100% - 39px);
      overflow: hidden;
      .el-tab-pane {
        height: 100%;
        margin: 0px;
        padding: 0px;
        iframe {
          border: none;
          width: 100%;
          height: 100%;
        }
      }
    }
  }
}
</style>