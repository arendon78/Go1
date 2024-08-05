from manim import *

class SquareToCircle(Scene):
    def construct(self):
        square = Square()
        circle = Circle()
        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))

if __name__ == "__main__":
    from manim import config
    config.background_color = BLACK
    scene = SquareToCircle()
    scene.render()
