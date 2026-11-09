import chroma, gltf, opengl, vmath, windy, polyworld/shapes

let window = newWindow("Arrow keys: collect gold", ivec2(960, 640))
window.makeContextCurrent()
loadExtensions()

let render = newRenderer(window)
var
  batch = initShapeRenderer()
  player = vec3(0)
  goal = vec3(2, 0, 2)
  score = 0'i32
let camera = perspective(45'f, 1.5'f, 0.1'f, 50'f) *
  lookAt(vec3(8, 10, 8), vec3(0), vec3(0, 1, 0))

while not window.closeRequested:
  pollEvents()
  if window.buttonPressed[KeyLeft]: player.x -= 1
  if window.buttonPressed[KeyRight]: player.x += 1
  if window.buttonPressed[KeyUp]: player.z -= 1
  if window.buttonPressed[KeyDown]: player.z += 1
  player = clamp(player, vec3(-4, 0, -4), vec3(4, 0, 4))

  if player == goal:
    inc score
    window.title = "Collected: " & $score
    goal = ivec3((score * 3) mod 9 - 4, 0, (score * 5) mod 9 - 4).vec3

  render.beginFrame(window, window.size)
  render.clearScreen(color(0.04, 0.05, 0.08, 1))
  batch.clear()
  batch.addSquare(vec3(0), 10, rgbx(40, 55, 70, 255))
  batch.addHexagon(goal, 0.35, rgbx(255, 190, 75, 255))
  batch.addCircle(player, 0.35, rgbx(90, 200, 255, 255))
  batch.draw(camera)
  render.endFrame()
  window.swapBuffers()

batch.closeShapeRenderer()
window.close()
