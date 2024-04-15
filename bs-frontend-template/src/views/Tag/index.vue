<template>
    <Page>
        <el-card>
            <template #header>
                <div class="card-header">
                    <span>Movie categories</span>
                </div>
            </template>
            <div class="tags">
                <span v-for="t in tags" :key="t.id">
                    <el-button
                        type="text"
                        style="font-size:20px;"
                        @click="toRoute(t.id)"
                    >{{ t.name }}</el-button>
                </span>
            </div>
        </el-card>
    </Page>
</template>

<script>
import request from "/@/utils/request"
import Page from "/@/components/Page/index.vue"
export default {
    components: { Page },
    data() {
        return {
            tags: [],
        }
    },
    created() {
        this.get_tags()
    },
    methods: {
        async get_tags() {
            let { data: { Data } } = await request.get('all_tags/')
            this.tags = Data
        },
        toRoute(tag) {
            this.$router.replace({ name: "Index", query: { tag } })
        }
    }
}
</script>
<style lang="postcss" scoped>
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
    span {
        display: inline-flex;
        justify-content: center;
        width: 24%;
    }
}
</style>