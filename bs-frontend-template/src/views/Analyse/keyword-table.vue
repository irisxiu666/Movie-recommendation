<template>
  <el-table :data="keywords" style="width: 100%">
    <el-table-column label="title" align="center">
      <template #default="scope">
        <p v-text="scope.row[1]"></p>
      </template>
    </el-table-column>
    <el-table-column label="weight" align="center">
      <template #default="scope">
        <p v-text="scope.row[0].toFixed(2)"></p>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import request from "/@/utils/request";
export default {
  props: ["text"],
  data() {
    return {
      keywords: [],
    };
  },
  mounted() {
    request.get(`/comment/keywords/${this.text}`).then((res) => {
      this.keywords = res.data;
    });
  },
};
</script>