
from manim import *
import numpy as np


class NeuralSignalFlow(Scene):

    def construct(self):

        # =====================================
        # 1. 背景とタイトル
        # =====================================

        self.camera.background_color = "#050B17"

        title = Text(
            "NEURAL SIGNAL FLOW",
            font_size=32,
            color=WHITE
        ).to_edge(UP)

        subtitle = Text(
            "Visualizing Forward Propagation",
            font_size=18,
            color="#83A9C9"
        ).next_to(title, DOWN)

        self.play(
            FadeIn(title),
            FadeIn(subtitle),
            run_time=1
        )

        # =====================================
        # 2. ニューラルネットワークの構築
        # =====================================

        # 各層のニューロン数
        layer_sizes = [4, 5, 5, 3]

        # ニューロンを層ごとに保存
        layers = []

        # 層と層の間の接続線を保存
        connection_groups = []

        for i, count in enumerate(layer_sizes):

            layer = VGroup()

            for j in range(count):

                # 画面上の座標を計算
                x = (i - 1.5) * 3
                y = (j - (count - 1) / 2) * 0.75

                # ニューロンの外側の円
                neuron = Circle(
                    radius=0.13,
                    stroke_color="#4DA6FF",
                    stroke_width=2,
                    fill_color="#0B2440",
                    fill_opacity=1
                )

                neuron.move_to([x, y, 0])

                layer.add(neuron)

            layers.append(layer)

        # =====================================
        # 3. ニューロン間の接続線
        # =====================================

        for i in range(len(layers) - 1):

            connections = VGroup()

            for start in layers[i]:
                for end in layers[i + 1]:

                    line = Line(
                        start.get_center(),
                        end.get_center(),
                        stroke_color="#4B7199",
                        stroke_width=1,
                        stroke_opacity=0.28
                    )

                    connections.add(line)

            connection_groups.append(connections)

        # 接続線を先に描画
        for group in connection_groups:
            self.play(
                Create(group),
                run_time=0.4
            )

        # ニューロンを順番に表示
        for layer in layers:
            self.play(
                FadeIn(layer, scale=0.5),
                run_time=0.35
            )

        self.wait(0.5)

        # =====================================
        # 4. 光の信号を生成
        # =====================================

        def create_signal():

            # 光の中心
            core = Dot(
                radius=0.045,
                color=WHITE
            )

            # 内側の光
            inner_glow = Dot(
                radius=0.09,
                color="#55C8FF",
                fill_opacity=0.45
            )

            # 外側の光
            outer_glow = Dot(
                radius=0.17,
                color="#3399FF",
                fill_opacity=0.12
            )

            # 3つの円を重ねて1つの粒子にする
            return VGroup(
                outer_glow,
                inner_glow,
                core
            )

        # =====================================
        # 5. 信号を層から層へ伝播
        # =====================================

        for layer_index, connections in enumerate(
            connection_groups
        ):

            signals = VGroup()

            animations = []

            # 接続線ごとに粒子を作る
            for line in connections:

                signal = create_signal()

                # 粒子を接続線の始点に配置
                signal.move_to(
                    line.get_start()
                )

                signals.add(signal)

                # 接続線に沿って粒子を移動
                animations.append(
                    MoveAlongPath(
                        signal,
                        line,
                        rate_func=smooth
                    )
                )

            # 粒子を画面に追加
            self.add(signals)

            # 接続線を明るくする
            self.play(
                connections.animate.set_stroke(
                    color="#348AC7",
                    opacity=0.6
                ),
                run_time=0.2
            )

            # すべての粒子を同時に移動
            self.play(
                *animations,
                run_time=1.3
            )

            # 到着した層のニューロンを発光
            target_layer = layers[layer_index + 1]

            self.play(
                *[
                    neuron.animate.set_fill(
                        "#55C8FF",
                        opacity=1
                    )
                    for neuron in target_layer
                ],
                run_time=0.25
            )

            # 粒子を消す
            self.play(
                FadeOut(signals),
                run_time=0.2
            )

            # ニューロンを元の色に戻す
            self.play(
                *[
                    neuron.animate.set_fill(
                        "#0B2440",
                        opacity=1
                    )
                    for neuron in target_layer
                ],
                connections.animate.set_stroke(
                    color="#4B7199",
                    opacity=0.28
                ),
                run_time=0.3
            )

        # =====================================
        # 6. エンディング
        # =====================================

        end_text = Text(
            "FORWARD PROPAGATION COMPLETE",
            font_size=22,
            color="#77D7FF"
        ).to_edge(DOWN)

        self.play(
            FadeIn(end_text),
            run_time=0.8
        )

        self.wait(1.5)

        self.play(
            FadeOut(
                VGroup(
                    title,
                    subtitle,
                    end_text,
                    *layers,
                    *connection_groups
                )
            ),
            run_time=1.2
        )

