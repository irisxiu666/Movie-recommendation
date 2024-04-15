export type ITag = 'Home' | 'Company' | 'School' | 'Supermarket'
export interface IRenderTableList {
    date: string
    name: string
    address: string
    tag: ITag
    amt: number
}