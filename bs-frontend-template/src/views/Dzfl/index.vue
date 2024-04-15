<template>
  <div style="padding: 30px">
    <el-row type="flex" justify="center">
      <vue-echarts :api="api" style="height: 700px"></vue-echarts>
    </el-row>
    <el-row type="flex" justify="center">
      <el-radio-group v-model="field">
        <el-radio
          :label="value"
          v-for="(label, value) in fields"
          :key="value"
          >{{ label }}</el-radio
        >
      </el-radio-group>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from "vue";
const field = ref("jyrs");
const fields = reactive({
  jyrs: "借阅人数",
  yxdzrs: "当前有效读者人数",
  jycs: "借阅册次",
  jyrrcs: "借阅人日次数",
});
const api = computed(() => {
  return `/dzfl/pie/?field=${field.value}`;
});
</script>