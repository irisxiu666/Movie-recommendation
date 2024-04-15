<template>
  <div class="w-screen h-screen bg-gray-200 flex justify-center items-center">
    <div class="layout-login" @keyup="enterSubmit">
      <h3
        class="text-2xl font-semibold text-gray-700 text-center mb-6"
      >Movie Recommendation System</h3>
      <el-form
        ref="ruleForm"
        label-position="right"
        label-width="80px"
        :model="form"
        :rules="rules"
      >
        <el-form-item class="mb-6 -ml-20" prop="name">
          <el-input v-model="form.name" placeholder="Please enter username" prefix-icon="el-icon-user" />
        </el-form-item>
        <el-form-item class="mb-6 -ml-20" prop="pwd">
          <el-input
            v-model="form.pwd"
            placeholder="Please enter password"
            prefix-icon="el-icon-lock"
            show-password
          />
        </el-form-item>
        <el-form-item class="mb-6 -ml-20" prop="pwd2">
          <el-input
            v-model="form.pwd2"
            placeholder="Please enter password again"
            prefix-icon="el-icon-lock"
            show-password
          />
        </el-form-item>
        <el-form-item class="mb-6 -ml-20">
          <el-button type="primary" class="w-full" @click="onSubmit">signup</el-button>
        </el-form-item>
        <el-link type="info" :underline="false" class="text-xs" @click="toPage('Login')">Already have an account? Login now</el-link>
      </el-form>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from "vue";
import { useLayoutStore } from "/@/store/modules/layout";
import { ElNotification } from "element-plus";
import { validate } from "/@/utils/formExtend";

const formRender = () => {
  const { register } = useLayoutStore();
  let form = reactive({
    name: "",
    email: "",
    pwd: "",
    pwd2: "",
  });
  const ruleForm = ref(null);
  const enterSubmit = (e: KeyboardEvent) => {
    if (e.key === "Enter") {
      onSubmit();
    }
  };
  const onSubmit = async () => {
    let { name, pwd, pwd2, email } = form;
    if (!(await validate(ruleForm))) return;
    await register({ username: name, password1: pwd, password2: pwd2, email });
    ElNotification({
      title: "Message",
      message: "Signup successfully",
      type: "success",
    });
  };
  const rules = reactive({
    name: [
      {
        validator: (
          rule: any,
          value: any,
          callback: (arg0?: Error | undefined) => void
        ) => {
          if (!value) {
            return callback(new Error("Username cannot be empty"));
          }
          callback();
        },
        trigger: "blur",
      },
    ],
    pwd: [
      {
        validator: (
          rule: any,
          value: any,
          callback: (arg0?: Error | undefined) => void
        ) => {
          if (!value) {
            return callback(new Error("Password cannot be empty"));
          }
          callback();
        },
        trigger: "blur",
      },
    ],
    pwd2: [
      {
        required: true,
        message: "Confirm password can not be empty",
        trigger: "blur",
      },
      {
        validator: (
          rule: any,
          value: string,
          callback: (arg0?: Error | undefined) => void
        ) => {
          if (value !== form.pwd) {
            callback(new Error("inconsistent passwords"))
          }
          callback();
        },
        trigger: "blur",
      },
    ],
  });
  return {
    form,
    onSubmit,
    enterSubmit,
    rules,
    ruleForm,
  };
};
export default defineComponent({
  name: "Login",
  setup() {
    return {
      labelCol: { span: 4 },
      wrapperCol: { span: 14 },
      ...formRender(),
    };
  },
});
</script>

<style lang='postcss' scoped>
.layout-login {
  width: 450px;
  padding: 60px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgb(0 0 0 / 10%);

  /* ::v-deep(.el-input__inner) {
    border: 1px solid hsla(0, 0%, 100%, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #ddd;
  } */
}
</style>