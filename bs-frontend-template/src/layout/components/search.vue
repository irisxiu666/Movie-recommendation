<template>
    <div
        class="layout-navbar-search hidden-xs-only cursor-pointer flex flex-center px-2"
        :class="{ 'open': isShow }"
    >
        <svg-icon class-name="svg-icon" icon-class="svg-search" @click.stop="changeStatus" />
        <div class="layout-navbar-search-select">
            <el-select
                ref="elSelect"
                v-model="href"
                filterable
                placeholder="Search movies..."
                remote
                :remote-method="searchText"
                @change="changeRoute"
            >
                <el-option
                    v-for="item in searchList"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id"
                />
            </el-select>
        </div>
    </div>
</template>
<script lang='ts'>
import { defineComponent, Ref, ref, watch } from 'vue'
// import { useLayoutStore } from '/@/store/modules/layout'
// import { IMenubarList, ISetting } from '/@/type/store/layout'
import { useRouter } from 'vue-router'
// import Fuse from 'fuse.js'
import request from '/@/utils/request'

// 不使用则不加载
// const pinyin = () => import('pinyin')

type ISearchList = any
// search显示隐藏状态
const changeSearchStatus = (searchList: Ref<ISearchList[]>) => {
    const router = useRouter()
    const href = ref('')
    const isShow = ref(false)
    const elSelect = ref()
    const changeStatus = () => {
        isShow.value = !isShow.value
        if (isShow.value && elSelect.value) {
            elSelect.value.focus()
        }
    }

    const hideSearch = () => {
        href.value = ''
        searchList.value.splice(0, searchList.value.length)
        isShow.value = false
    }

    watch(isShow, (newValue) => {
        if (newValue) {
            document.body.addEventListener('click', hideSearch)
        } else {
            document.body.removeEventListener('click', hideSearch)
        }
    })

    const changeRoute = () => {
        router.push({ name: 'Detail', params: { id: href.value } })
    }

    return {
        href,
        changeRoute,
        changeStatus,
        isShow,
        elSelect,
        hideSearch
    }
}

export default defineComponent({
    name: 'Search',
    setup() {
        // const { getMenubar, getSetting } = useLayoutStore()
        const searchList: Ref<ISearchList[]> = ref([])
        const searchText = async (query: string) => {
            if (query !== '') {
                request.post('search_movies/', { keyword: query }).then(res => {
                    searchList.value = res.data.Data
                })
            } else {
                searchList.value = []
            }
        }
        // search(searchList, getMenubar.menuList, getSetting).then(data => {
        //     searchText.value = data
        // })

        return {
            searchList,
            searchText,
            ...changeSearchStatus(searchList)
        }
    }
})
</script>

<style lang='postcss' scoped>
::v-deep(.el-input__inner) {
    border-top: none;
    border-left: none;
    border-right: none;
    border-radius: 0;
}

::v-deep(.el-select__caret) {
    display: none;
}

.layout-navbar-search {
    .layout-navbar-search-select {
        transition: width 0.2s;
        width: 0;
        overflow: hidden;
    }

    &.open {
        .layout-navbar-search-select {
            width: 210px;
        }
    }
}
</style>