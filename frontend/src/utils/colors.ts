export function hexToRgb(hex: string): number[] | null {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  return result ? [
    parseInt(result[1], 16),
    parseInt(result[2], 16),
    parseInt(result[3], 16)
  ] : null
}

export function rgbToHex(color: number[]): string {
  return "#" + (1 << 24 | color[0] << 16 | color[1] << 8 | color[2]).toString(16).slice(1);
}

export function setCssStyle(name: string, value: string): void {
  document.documentElement.style.setProperty(name, value)
}

export function mixColors(fg: number[], bg: number[], opacity = 0.7): number[] {
  return fg.map((x, i) => x * opacity + (1 - opacity) * bg[i])
}

export function isLightTheme(): boolean {
  const themeParams = window.Telegram.WebApp.themeParams
  const bgColor = hexToRgb(themeParams.bg_color)

  if (bgColor === null) {
    return true
  } else {
    const meanColor = bgColor.reduce((p, c) => p + c, 0) / 3
    return meanColor > 255 / 2
  }
}
