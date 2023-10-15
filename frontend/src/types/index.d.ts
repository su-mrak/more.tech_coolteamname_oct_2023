/// <reference types="vite-plugin-svgr/client" />

export {}

type openLinkOptions = {try_instant_view: boolean} | undefined

interface PopupButton {
  id: string,
  type: "default" | "ok" | "close" | "cancel" | "destructive",
  text: string,
}

interface PopupParams {
  title: string,
  message: string,
  buttons: PopupButton[],
}

interface WebAppUser {
  id: number,
  is_bot?: boolean,
  first_name: string,
  last_name?: string,
  username?: string,
  language_code?: string,
  is_premium?: boolean,
  photo_url?: string,
}

interface WebAppChat {
  id: number,
  type: "group" | "supergroup" | "channel",
  title: string,
  username?: string,
  photo_url?: string,
}

interface WebAppInitData {
  query_id?: string,
  user?: WebAppUser,
  receiver?: WebAppUser,
  chat?: WebAppChat,
  chat_type?: "private" | "group" | "supergroup" | "channel",
  chat_instance?: string,
  start_param?: string,
  can_send_after?: number,
  auth_date: number,
  hash: string,
}

interface ThemeParams {
  bg_color: string,
  text_color: string,
  hint_color: string,
  link_color: string,
  button_color: string,
  button_text_color: string,
  secondary_bg_color: string,

  border_color: string,
  button_hover_color: string,
  danger_color: string,
}

interface BackButton {
  isVisible: boolean,
  onClick: (callback: () => void) => void,
  offClick: (callback: () => void) => void,
  show: () => void,
  hide: () => void,
}

interface MainButton {
  text: string,
  color: string,
  textColor: string,
  isVisible: boolean,
  isActive: boolean,
  isProgressVisible: boolean,
  setText: (text: string) => void,
  onClick: (callback: () => void) => void,
  offClick: (callback: () => void) => void,
  show: () => void,
  hide: () => void,
  enable: () => void,
  disable: () => void,
  showProgress: (leaveActive: boolean) => void,
  hideProgress: () => void,
  setParams: (params: {
    text?: string, color?: string, text_color?: string,
    is_active?: boolean, is_visible?: boolean,
  }) => void,
}

interface HapticFeedback {
  impactOccurred: (style: "light" | "medium" | "heavy" | "rigid" | "soft") => void,
  notificationOccurred: (type: "success" | "warning" | "error") => void,
  selectionChanged: () => void,
}

interface ScanQRPopupParams {
  text: string,
}

interface Telegram {
  WebApp: {
    initData: string,
    initDataUnsafe: WebAppInitData,
    version: string,
    platform: string,

    colorScheme: string,
    themeParams: ThemeParams,

    isExpanded: boolean,
    viewportHeight: number,
    viewportStableHeight: number,

    headerColor: string,
    backgroundColor: string,

    isClosingConfirmationEnabled: boolean,

    BackButton: BackButton,
    MainButton: MainButton,
    HapticFeedback: HapticFeedback,

    isVersionAtLeast(version: string): boolean,
    setHeaderColor(color: string): void,
    setBackgroundColor(color: string): void,
    enableClosingConfirmation(): void,
    disableClosingConfirmation(): void,

    onEvent(eventType: string, eventHandler: () => void): void,
    offEvent(eventType: string, eventHandler: () => void): void,

    sendData(data: string): void,

    switchInlineQuery(query: string, choose_chat_types?: boolean): void,
    openLink(url: string, options?: openLinkOptions): void,
    openTelegramLink(url: string): void,
    openInvoice(url: string, callback?: (id: string) => void): void,

    showPopup(params: PopupParams, callback?: (id: string) => void): void,
    showAlert(message: string, callback?: () => void): void,
    showConfirm(message: string, callback?: (ok: boolean) => void): void,

    showScanQRPopup(params: ScanQRPopupParams, callback?: (result: string) => void): void,
    closeScanQRPopup(): void,
    readTextFromClipboard(callback?: (text: string) => void): void,

    ready(): void,
    expand(): void,
    close(): void,
  }
}

declare global {
  interface Window {
    Telegram: Telegram
  }
}
