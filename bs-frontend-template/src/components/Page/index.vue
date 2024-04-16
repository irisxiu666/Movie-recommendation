<template>
    <div class="x-container">
        <div class="inner">
            <div class="content">
                <slot />
            </div>
            <div class="right">
                <slot name="right">
                    <el-card class="recent" shadow="always">
                        <template #header>
                            <div class="card-header">
                                <span>Recent updates</span>
                            </div>
                        </template>
                        <el-button
                            type="text"
                            v-for="m in recent_movies"
                            :key="m.id"
                            style="margin-bottom:10px;display:block;margin-left:0;text-align:left"
                            @click="toDetail(m.id)"
                        >{{ m.name }}</el-button>
                    </el-card>
                    <el-card class="user-recommand" shadow="always">
                        <template #header>
                            <div class="card-header">
                                <span>Recommend movies</span>
                                <el-button
                                    class="button"
                                    type="primary"
                                    size="mini"
                                    @click="get_user_recommend"
                                >Another batch</el-button>
                            </div>
                        </template>
                        <div
                            v-for="m in user_recommend"
                            :key="m.id"
                            class="movie-card-simple"
                            @click="toDetail(m.id)"
                            style="cursor:pointer;"
                        >
                            <img class="cover" v-src="m.image_link" />
                            <div class="desc">
                                <el-button
                                    type="text"
                                    style="margin-bottom:10px;display:block;text-align:left"
                                >{{ m.name }}</el-button>
                                <p>{{ m.years }}</p>
                                <p>Rating: {{ m.d_rate }}</p>
                            </div>
                        </div>
                    </el-card>
                </slot>
            </div>
        </div>
    </div>
</template>

<script>
import request from "/@/utils/request"
export default {
    data() {
        return {
            recent_movies: [],
            user_recommend: []
        }
    },
    created() {
        this.get_recent_movies()
        this.get_user_recommend()
    },
    methods: {
        toDetail(id) {
            this.$router.push({ name: 'Detail', params: { id } })
        },
        async get_recent_movies() {
            let { data: { Data } } = await request.get('recent_movies/')
            this.recent_movies = Data
        },
        async get_user_recommend() {
            let { data: { Data } } = await request.get('user_recommend/')
            this.user_recommend = Data
        }
    }
}
</script>

<style lang="postcss" scoped>
.movie-card-simple {
    cursor: pointer;
    display: flex;
    margin: 15px 10px;
    img.cover {
        max-width: 130px;
    }
    .desc {
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
.column {
    display: flex;
    flex-direction: column;
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
.x-container {
    padding: 60px 30px;
    display: flex;
    justify-content: center;
    .inner {
        width: 80%;
        display: flex;
        .content {
            flex: 1;
        }
        .right {
            width: 25%;
            margin-left: 30px;
            .recent {
                margin-bottom: 20px;
            }
        }
    }
}
</style>