from manim import *
import numpy as np


class NeuralNetwork(Scene):
    def construct(self):

        # 各層のニューロン数
        layers = [4, 5, 5, 2]

        # ニューロンと接続線を保存する
        neurons = []
        connections = VGroup()

        # ニューロンを配置
        for i, count in enumerate(layers):
            layer = VGroup()

            for j in range(count):
                # 円の位置を計算
                x = (i - 1.5) * 2.2
                y = (j - (count - 1) / 2) * 0.8

                neuron = Circle(radius=0.15, color=BLUE, stroke_width=2)

                neuron.move_to([x, y, 0])
                layer.add(neuron)

            neurons.append(layer)

        # 隣接する層のニューロンを接続
        for i in range(len(neurons) - 1):
            for start in neurons[i]:
                for end in neurons[i + 1]:
                    line = Line(
                        start.get_center(),
                        end.get_center(),
                        color=GRAY,
                        stroke_opacity=0.3,
                    )

                    connections.add(line)

        # 接続線を表示
        self.play(Create(connections), run_time=2)

        # ニューロンを表示
        for layer in neurons:
            self.play(Create(layer), run_time=0.5)

        # 信号が左から右へ伝わる様子
        for layer in neurons:
            self.play(
                *[neuron.animate.set_fill(YELLOW, opacity=1) for neuron in layer],
                run_time=0.5,
            )

            self.play(
                *[neuron.animate.set_fill(BLUE, opacity=0) for neuron in layer],
                run_time=0.3,
            )

        self.wait(1)
