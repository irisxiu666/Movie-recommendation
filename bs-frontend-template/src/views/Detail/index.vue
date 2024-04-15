<template>
    <Page v-if="detail">
        <div class="info">
            <img v-src="detail.image_link" />
            <el-descriptions :column="2">
                <el-descriptions-item label="Movie name:">{{ detail.name }}</el-descriptions-item>
                <el-descriptions-item label="Publish date:">{{ detail.years }}</el-descriptions-item>
                <el-descriptions-item label="Director:">{{ detail.director }}</el-descriptions-item>
                <el-descriptions-item label="Starring:">{{ wrapText(detail.leader, 20) }}</el-descriptions-item>
                <el-descriptions-item label="Rating:">{{ detail.d_rate }}</el-descriptions-item>
                <el-descriptions-item label="Number of collectors:">{{ detail.collect_count }}</el-descriptions-item>
                <el-descriptions-item label="Tag:">
                    <el-tag
                        style="margin-right:5px;cursor:pointer"
                        v-for="t in detail.all_tags"
                        :key="t.id"
                        type="info"
                        effect="plain"
                        @click="toRoute(t.id)"
                    >{{ t.name }}</el-tag>
                </el-descriptions-item>
                <el-descriptions-item>
                    <el-link
                        :href="`https://v.qq.com/x/search/?q=${detail.name}&stag=0&smartbox_ab=`"
                        target="_blank"
                        type="success"
                        style="font-size:25px"
                    >Go to watch</el-link>
                </el-descriptions-item>
                <el-descriptions-item label="Add ratings">
                    <template v-if="detail.user_rate == null">
                        <el-select size="mini" v-model="score">
                            <el-option v-for="i in 5" :label="i" :key="i" :value="i"></el-option>
                        </el-select>
                        <el-button
                            type="primary"
                            size="mini"
                            style="margin-left:10px;"
                            @click="addScore"
                        >submit</el-button>
                    </template>
                    <span v-else>You have rated: {{ detail.user_rate.mark }}</span>
                </el-descriptions-item>
                <el-descriptions-item>
                    <el-button
                        size="large"
                        type="primary"
                        @click="collect"
                        v-if="detail.is_collect == null"
                    >Click to collect</el-button>
                    <el-button size="large" type="warning" @click="decollect" v-else>Cancel collection</el-button>
                </el-descriptions-item>
            </el-descriptions>
        </div>
        <div class="desc">{{ detail.intro }}</div>
        <el-card class="item-recommand" shadow="always">
            <template #header>
                <div class="card-header">
                    <span>Recommend movies based on items</span>
                    <el-button
                        class="button"
                        type="primary"
                        size="mini"
                        @click="get_item_recommend"
                    >Change a batch</el-button>
                </div>
            </template>
            <div
                v-for="m in item_recommend"
                :key="m.id"
                class="movie-card-simple"
                @click="toDetail(m.id)"
                style="cursor:pointer;"
            >
                <img class="cover" v-src="m.image_link" />
                <div class="desc2">
                    <el-button
                        type="text"
                        style="margin-bottom:10px;display:block;text-align:left"
                    >{{ m.name }}</el-button>
                    <p>{{ m.years }}</p>
                </div>
            </div>
        </el-card>
        <div class="comment-part">
            <div style="display:flex;">
                <el-input placeholder="Come on, tell me something~" style="flex:1" v-model="comment"></el-input>
                <el-button
                    :disabled="comment.length === 0"
                    type="success"
                    size="large"
                    style="margin-left:10px;"
                    @click="makeComment"
                >submit comments</el-button>
            </div>
            <el-tabs type="card" style="margin-top:10px;">
                <el-tab-pane label="comment">
                    <template v-if="detail.comments.length != 0">
                        <div v-for="c in detail.comments" class="comment-card" :key="c.id">
                            <el-avatar shape="square" :size="50">{{ c.userName }}</el-avatar>
                            <div class="wrap">
                                <p>{{ c.content }}</p>
                                <p>{{ c.userName }} published at {{ formatDateTime(new Date(c.create_time)) }}</p>
                            </div>
                        </div>
                    </template>
                    <h1
                        v-else
                        style="font-weight:bold;color:#888,font-size:25px;text-align:center;"
                    >No comments</h1>
                </el-tab-pane>
            </el-tabs>
        </div>
    </Page>
</template>

<script>
import { formatDateTime } from "/@/utils/tools"
import request from "/@/utils/request"
import Page from "/@/components/Page/index.vue"
export default {
    props: {
        id: Number,
    },
    components: { Page },
    data() {
        return {
            item_recommend: [],
            detail: null,
            score: 1,
            comment: ''
        }
    },
    created() {
        this.get_movie()
        this.get_item_recommend()
    },
    methods: {
        formatDateTime,
        async makeComment() {
            await request.post(`comment/${this.detail.id}/`, { comment: this.comment })
            this.comment = ''
            this.$message.success('Commented successful')
            this.get_movie()
        },
        async collect() {
            await request.get(`collect/${this.detail.id}/`)
            this.$message.success('Collected successful')
            this.get_movie()
        },
        async decollect() {
            await request.get(`decollect/${this.detail.id}/`)
            this.$message.success('Cancel collection successfully')
            this.get_movie()
        },
        async addScore() {
            await request.post(`score/${this.detail.id}/`, { score: this.score })
            this.$message.success('Rated successfully')
            this.get_movie()
        },
        async get_item_recommend() {
            let { data: { Data } } = await request.get('item_recommend/')
            this.item_recommend = Data
        },
        async get_movie() {
            let { data: { Data } } = await request.get(`movie/${this.id}`)
            this.detail = Data
        },
        wrapText(text, limit = 50) {
            if (text.length > limit) {
                return text.substring(0, limit) + '...'
            } else {
                return text
            }
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
.comment-card {
    display: flex;
    margin-bottom: 10px;
    border-bottom: 1px dotted #ccc;
    padding: 20px 10px;
    .wrap {
        margin-left: 30px;
        flex: 1;
        p:nth-child(1) {
            font-weight: bold;
            margin-bottom: 20px;
        }
        p:nth-child(2) {
            color: #888;
            font-size: 14px;
        }
    }
}
.comment-part {
    margin-top: 30px;
}
.item-recommand {
    ::v-deep(.el-card__body) {
        display: flex;
    }
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
.info {
    display: flex;
    align-items: center;
    ::v-deep(.el-descriptions) {
        flex: 1;
        .el-descriptions__body {
            background-color: transparent !important;
            .el-descriptions__cell {
                font-size: 18px;
                .el-descriptions__label {
                    color: black;
                    font-weight: bold;
                }
            }
        }
    }
    img {
        width: 200px;
        margin-right: 10px;
    }
}
.desc {
    margin-top: 30px;
    margin-bottom: 30px;
    padding: 30px;
    box-shadow: 1px 1px 5px #ccc;
}
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    span {
        font-size: 20px;
        font-weight: bold;
    }
}
.movie-card-simple {
    flex: 1;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    margin: 15px 10px;
    img {
        width: 100%;
    }
    .desc2 {
        flex: 1;
        padding: 10px;
        p {
            font-size: 12px;
        }
        p + p {
            margin-top: 10px;
        }
    }
}
</style>