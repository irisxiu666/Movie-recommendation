import { App } from 'vue'

export default (app: App<Element>): void => {
    app.directive('src', {
        beforeMount(el, binding) {
            const { value } = binding
            const src = import.meta.env.VITE_API_BASE_URL.replace("api", "media/") + value
            el.setAttribute('src', src)
        },
    })
}