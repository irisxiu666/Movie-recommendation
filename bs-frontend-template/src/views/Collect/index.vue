<template>
    <Page>
        <el-card>
            <template #header>
                <div class="card-header">
                    <span>My collections</span>
                </div>
            </template>
            <el-table :data="records" style="width: 100%">
                <el-table-column prop="name" label="Movie name">
                    <template #default="{ row }">
                        <el-button type="text" @click="toDetail(row.id)">{{ row.name }}</el-button>
                    </template>
                </el-table-column>
                <el-table-column prop="director" label="Director"></el-table-column>
                <el-table-column prop="tags" label="Tag">
                    <template #default="{ row: { all_tags } }">
                        <el-tag
                            style="margin-right:5px;cursor:pointer"
                            v-for="t in all_tags"
                            :key="t.id"
                            type="info"
                            effect="plain"
                            @click="toRoute(t.id)"
                        >{{ t.name }}</el-tag>
                    </template>
                </el-table-column>
            </el-table>
        </el-card>
    </Page>
</template>

<script>
import { formatDateTime } from "/@/utils/tools"
import request from "/@/utils/request"
import Page from "/@/components/Page/index.vue"
export default {
    components: { Page },
    data() {
        return {
            records: [],
        }
    },
    created() {
        this.get_records()
    },
    methods: {
        formatDateTime,
        async get_records() {
            let { data: { Data } } = await request.get('mycollect/')
            this.records = Data
        },
        toRoute(tag) {
            this.$router.replace({ name: "Index", query: { tag } })
        },
        toDetail(id) {
            this.$router.push({ name: 'Detail', params: { id } })
        },
    }
}
</script>
<style lang="postcss" scoped>
h1 {
    font-size: 20px;
}
.card-header {
    display: flex;
    justify-content: center;
    align-items: center;
    span {
        font-size: 30px;
        font-weight: bold;
    }
}
.tags {
    width: 100%;
    display: inline-flex;
    flex-wrap: wrap;
}
</style>