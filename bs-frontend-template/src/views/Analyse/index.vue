<template>
  <div style="padding: 30px">
    <el-row type="flex" justify="center">
      <el-form :model="commentForm" :inline="true">
        <el-form-item label="username">
          <el-input
            v-model="commentForm._username__icontains"
            clearable
          ></el-input>
        </el-form-item>
        <el-form-item label="comments">
          <el-input v-model="commentForm._text__icontains" clearable></el-input>
        </el-form-item>
        <el-form-item label="Sentiment classification">
          <el-select
            v-model="commentForm._positive"
            clearable
            placeholder="Please select"
          >
            <el-option :value="true" label="正面"></el-option>
            <el-option :value="false" label="负面"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            @click="
              commentForm.page = 1;
              searchComment();
            "
            >Search</el-button
          >
        </el-form-item>
      </el-form>
    </el-row>
    <el-table :data="commentList" style="width: 100%; margin: 20px 10px">
      <el-table-column
        label="Username"
        prop="username"
        align="center"
      ></el-table-column>
      <el-table-column
        label="Comments"
        prop="text"
        align="center"
      ></el-table-column>
      <el-table-column
        label="Publish time"
        prop="publish_time"
        align="center"
      ></el-table-column>
      <el-table-column label="Sentiment classification" align="center">
        <template #default="scope">
          <el-tag :type="scope.row.positive ? 'success' : 'danger'">
            {{ scope.row.positive ? "Positive emotion" : "Negative emotion" }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="Positive emotion probability" align="center">
        <template #default="scope">
          {{ scope.row.prob.toFixed(2) }}
        </template>
      </el-table-column>
      <el-table-column label="operation" align="center">
        <template #default="scope">
          <el-button @click="viewCommentDetail(scope.row.text)" type="primary"
            >Detailed analysis</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <el-row type="flex" justify="center" style="margin-top: 30px">
      <el-pagination
        @current-change="handleCurrentChange2"
        :current-page="commentForm.page"
        :page-size="commentForm.pagesize"
        layout="prev, pager, next, jumper, total"
        :total="commentForm.total"
        background
      >
      </el-pagination>
    </el-row>
    <el-dialog
      title="Detailed analysis content"
      v-model="centerDialogVisible"
      width="70%"
      destroy-on-close
      center
    >
      <h3 style="text-align: center">comments: {{ dialogDatas.text }}</h3>
      <el-card
        shadow="always"
        style="margin-bottom: 20px; background-color: #f6f6f6"
      >
        <p><strong>part of speech analysis:</strong></p>
        <my-tag
          v-for="(t, index) in dialogDatas.tags"
          :val="t"
          :key="index"
        ></my-tag>
      </el-card>
      <el-card
        shadow="always"
        style="margin-bottom: 20px; background-color: #f6f6f6"
      >
        <p>
          <strong>emotion analysis:</strong> 0~0.5之间判断为负面，0.5~1之间判断为正面。
        </p>
        <vue-echarts
          :api="dialogDatas.commentApi"
          style="width: 600px; height: 400px"
        ></vue-echarts>
      </el-card>
      <el-card
        shadow="always"
        style="margin-bottom: 20px; background-color: #f6f6f6"
      >
        <p><strong>Keyword extraction:</strong></p>
        <keyword-table :text="dialogDatas.text"></keyword-table>
      </el-card>
    </el-dialog>
  </div>
</template>

<script>
import request from "/@/utils/request";
import { formatDateTime } from "/@/utils/tools";
import MyTag from "./my-tag.vue";
import KeywordTable from "./keyword-table.vue";
export default {
  data() {
    return {
      commentList: [],
      commentForm: {
        _username__icontains: null,
        _text__icontains: null,
        _positive: null,
        total: 0,
        page: 1,
        pagesize: 10,
      },
      centerDialogVisible: false,
      dialogDatas: {
        commentApi: null,
        text: null,
        tags: [],
      },
    };
  },
  beforeMount() {
    this.searchComment();
  },
  methods: {
    viewCommentDetail(text) {
      this.centerDialogVisible = true;
      this.dialogDatas.commentApi = `/comment/pie/${text}`;
      this.dialogDatas.text = text;
      request.get(`/comment/tag/${text}`).then((res) => {
        this.dialogDatas.tags = res.data;
      });
    },
    handleCurrentChange2(page) {
      this.commentForm.page = page;
      this.searchComment();
    },
    searchComment() {
      request.post("/comments/", this.commentForm).then((res) => {
        this.commentList = res.data.result;
        this.commentForm.total = res.data.total;
      });
    },
  },
  components: {
    MyTag,
    KeywordTable,
  },
};
</script>