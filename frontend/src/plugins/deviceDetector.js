export default {
  install(app) {
    const isMobile = /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent)
    const deviceType = isMobile ? 'mobile' : 'desktop'

    // 1. 加到 document.body 的 class
    document.body.classList.add(`${deviceType}-ui`)

    // 2. 全域提供一個變數
    app.config.globalProperties.$deviceType = deviceType
  },
}
