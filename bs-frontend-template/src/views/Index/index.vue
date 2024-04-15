<template>
    <Page>
        <el-card>
            <template #header>
                <div class="card-header">
                    <span>{{ title }}</span>
                    <div>
                        <el-select
                            clearable
                            filterable
                            class="button"
                            type="primary"
                            size="large"
                            @change="changeOrder"
                            v-model="form.tag"
                            placeholder="Movie Tag"
                        >
                            <el-option v-for="t in tags" :key="t.id" :label="t.name" :value="t.id"></el-option>
                        </el-select>

                        <el-select
                            style="margin-left:10px;"
                            class="button"
                            type="primary"
                            size="large"
                            @change="changeOrder"
                            v-model="form.order"
                        >
                            <el-option
                                v-for="label, key in orders"
                                :key="key"
                                :label="label"
                                :value="key"
                            ></el-option>
                        </el-select>
                    </div>
                </div>
            </template>
            <div class="movies">
                <el-card
                    class="movie"
                    shadow="hover"
                    v-for="m in movies"
                    :key="m.id"
                    @click="toDetail(m.id)"
                    style="cursor:pointer;"
                >
                    <img v-src="m.image_link" />
                    <el-button type="text">{{ m.name }}</el-button>
                    <span style="text-align:center;font-size:12px">{{ m.years }}</span>
                </el-card>
            </div>
            <div style="display:flex;justify-content:center;margin-top:30px;">
                <el-pagination
                    @current-change="handleCurrentChange"
                    :current-page="form.page"
                    :page-size="form.pagesize"
                    layout="prev, pager, next, jumper, total"
                    :total="form.total"
                    background
                ></el-pagination>
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
            movies: [],
            tags: [],
            form: {
                tag: null,
                order: 'num',
                page: 1,
                pagesize: 15,
                total: 0,
            },
            orders: {
                collect: 'Collection sorting',
                rate: 'Rating sorting',
                years: 'Time sorting',
                num: 'Popularity sorting',
            }
        }
    },
    async created() {
        await this.get_tags()
        this.form.tag = this.$route.query.tag
        if (this.form.tag) {
            this.form.tag = Number(this.form.tag)
        }
        await this.search()
    },
    computed: {
        title() {
            const t = this.tags.find((v) => {
                return v.id === this.form.tag
            }) || {}
            return [t.name, this.orders[this.form.order]].filter(v => v).join(' - ')
        }
    },
    methods: {
        toDetail(id) {
            this.$router.push({ name: 'Detail', params: { id } })
        },
        handleCurrentChange(page) {
            this.form.page = page;
            this.search()
        },
        changeOrder() {
            this.form.page = 1
            this.search()
        },
        async search() {
            let { data: { Data: { total, results } } } = await request.post('movies/', this.form)
            this.movies = results
            this.form.total = total
        },
        async get_tags() {
            let { data: { Data } } = await request.get('all_tags/')
            this.tags = Data
        }
    }
}
</script>
<style lang="postcss" scoped>
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    span {
        font-size: 20px;
        font-weight: bold;
    }
}
.movies {
    display: inline-flex;
    flex-wrap: wrap;
    ::v-deep(.el-card) {
        width: 19%;
        margin: 0 10px 10px 0;
    }
    ::v-deep(.el-card__body) {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-content: center;
    }
}
</style>