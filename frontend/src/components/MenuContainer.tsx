import React, {useEffect, useRef, useState} from "react"
import "./MenuContainer.scss"
import Sheet, {SheetRef} from "react-modal-sheet"

interface Props {
  children: React.ReactNode
}

export default function MenuContainer(props: Props): React.JSX.Element {
  const {children} = props

  const sheetRef = useRef<SheetRef>()
  const [width, setWidth] = useState<number>(window.innerWidth)
  const isSmallScreen = width <= 768;

  const handleWindowSizeChange = () => {
    setWidth(window.innerWidth)
  }

  const handleClosePopup = () => {
    sheetRef.current?.snapTo(100)
  }

  useEffect(() => {
    window.addEventListener('resize', handleWindowSizeChange)
    return () => {
      window.removeEventListener('resize', handleWindowSizeChange)
    }
  }, [])

  if (isSmallScreen) {
    return (
      <Sheet
        ref={sheetRef}
        snapPoints={[-50, 0.5, 200]}
        initialSnap={1}
        isOpen={true}
        onClose={handleClosePopup}
      >
        <Sheet.Container>
          <Sheet.Header/>
          <Sheet.Content>
            <Sheet.Scroller>
              <div className="MenuContainer__content">
                {children}
              </div>
            </Sheet.Scroller>
          </Sheet.Content>
        </Sheet.Container>
      </Sheet>
    )
  } else {
    return (
      <div className="MenuContainer">
        {children}
      </div>
    )
  }
}
