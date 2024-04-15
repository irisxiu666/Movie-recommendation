<template>
    <Page>
        <el-card>
            <template #header>
                <div class="card-header">
                    <span>Choose your favorite tag</span>
                </div>
            </template>
            <div class="tags">
                <span v-for="t in tags" :key="t.id">
                    <el-tag style="cursor:pointer;margin:0 0 20px 0" size="large" @click="addTag(t.name)"
                        :effect="chosen.includes(t.name) ? 'dark' : 'plain'">
                        {{ t.name }}
                    </el-tag>
                    <!-- <el-button
                        type="text"
                        style="font-size:20px;"
                        @click="toRoute(t.id)"
                    >{{ t.name }}</el-button> -->
                </span>
            </div>
            <div class="flex justify-center">
                <el-button :disabled="chosen.length === 0" type="success" size="large" @click="submitChosen">submit
                </el-button>
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
            chosen: [],
            tags: [],
        }
    },
    created() {
        this.get_tags()
    },
    methods: {
        async submitChosen() {
            await request.post('choose_tags/', { tags_name: this.chosen })
            this.$message.success('Submitted successfully')
            this.$router.push('/')
        },
        addTag(name) {
            const idx = this.chosen.indexOf(name)
            if (idx === -1) {
                this.chosen.push(name)
            } else {
                this.chosen.splice(idx, 1)
            }
        },
        async get_tags() {
            let { data: { Data } } = await request.get('all_tags/')
            this.tags = Data.filter(v => {
                return Boolean(v.name)
            })
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