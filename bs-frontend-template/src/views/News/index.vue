<template>
  <div style="padding: 30px">
    <el-row type="flex" justify="center">
      <el-form :model="newsForm" :inline="true">
        <el-form-item label="title">
          <el-input v-model="newsForm._title__icontains" clearable></el-input>
        </el-form-item>
        <el-form-item label="content">
          <el-input v-model="newsForm._summary__icontains" clearable></el-input>
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            @click="
              newsForm.page = 1;
              searchNews();
            "
            >Search</el-button
          >
        </el-form-item>
      </el-form>
    </el-row>
    <el-row type="flex" justify="center">
      <el-timeline style="width: 80%">
        <el-timeline-item
          :timestamp="formatDateTime(news.pubDate)"
          placement="top"
          v-for="news in newsList"
          :key="news.id"
          size="large"
        >
          <el-link :href="news.sourceUrl" target="_blank" :underline="false">
            <el-card>
              <h4>{{ news.title }}</h4>
              <p>{{ news.summary }}</p>
              <el-tag type="info">来源: {{ news.infoSource }}</el-tag>
            </el-card>
          </el-link>
        </el-timeline-item>
      </el-timeline>
    </el-row>
    <el-row type="flex" justify="center" style="margin-top: 30px">
      <el-pagination
        @current-change="handleCurrentChange"
        :current-page="newsForm.page"
        :page-size="newsForm.pagesize"
        layout="prev, pager, next, jumper, total"
        :total="newsForm.total"
        background
      >
      </el-pagination>
    </el-row>
  </div>
</template>

<script>
import request from "/@/utils/request";
import { formatDateTime } from "/@/utils/tools";
export default {
  data() {
    return {
      newsList: [],
      newsForm: {
        _title__icontains: null,
        _summary__icontains: null,
        total: 0,
        page: 1,
        pagesize: 10,
      },
    };
  },
  methods: {
    formatDateTime,
    handleCurrentChange(page) {
      this.newsForm.page = page;
      this.searchNews();
    },
    searchNews() {
      request.post("/news/", this.newsForm).then((res) => {
        this.newsList = res.data.result;
        this.newsForm.total = res.data.total;
      });
    },
  },
  beforeMount() {
    this.searchNews();
  },
};
</script>