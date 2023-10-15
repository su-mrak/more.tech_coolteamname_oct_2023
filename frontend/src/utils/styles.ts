import rgba from "color-rgba"
import {mixColors, rgbToHex, setCssStyle} from "./"

export function setupStyles(): void {
  let themeParams = window.Telegram.WebApp.themeParams

  if (Object.keys(themeParams).length === 0) {
    // Using default color scheme
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      themeParams = {
        bg_color: "#212121",
        border_color: "rgba(170, 170, 170, .5)",
        button_color: "#8774e1",
        button_hover_color: "#685ba7",
        button_text_color: "#ffffff",
        hint_color: "#aaaaaa",
        link_color: "#8774e1",
        secondary_bg_color: "#181818",
        text_color: "#ffffff",
        danger_color: "#E50019"
      }
    } else {
      themeParams = {
        bg_color: "#ffffff",
        button_color: "#3390ec",
        button_text_color: "#ffffff",
        hint_color: "#707579",
        link_color: "#00488f",
        secondary_bg_color: "#f4f4f5",
        text_color: "#000000",
        button_hover_color: "#70b1f1",
        border_color: "rgba(112, 117, 121, .5)",
        danger_color: "#E50019"
      }
    }
  }

  const backgroundColor = rgba(themeParams.bg_color)
    ?.slice(0, 3) || [211, 211, 211]
  const hintColor = rgba(themeParams.hint_color)
    ?.slice(0, 3) || [100, 100, 100]
  const buttonColor = rgba(themeParams.button_color)
    ?.slice(0, 3) || [51, 144, 236]

  themeParams.button_hover_color = rgbToHex(mixColors(buttonColor, backgroundColor, .9))
  themeParams.border_color = `rgba(${hintColor.join(", ")}, .5)`

  for (const color in themeParams) {
    const cssVarName = `--tg-theme-${color.replace(/_/g, "-")}`

    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    setCssStyle(cssVarName, themeParams[color])
  }

  for (const color in themeParams) {
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    window.Telegram.WebApp.themeParams[color] = themeParams[color]
  }
}
