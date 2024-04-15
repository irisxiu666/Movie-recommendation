// import request from '/@/utils/request'
// import { AxiosResponse } from 'axios'
// const api = {
//     getTableList: '/api/getTableList'
// }
// export type ITag = 'All' | 'Home' | 'Company' | 'School' | 'Supermarket'
// export interface ITableList {
//     page: number
//     size: number
//     tag: ITag
// }
// export function getTableList(tableList: ITableList): Promise<AxiosResponse<IResponse>> {
//     return request({
//         url: api.getTableList,
//         method: 'get',
//         params: tableList
//     })
// }