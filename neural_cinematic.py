
from manim import *
import numpy as np


class CinematicNeuralNetwork(MovingCameraScene):

    def construct(self):

        # =====================================
        # 1. 映像の基本設定
        # =====================================

        self.camera.background_color = "#050B17"

        BLUE_LIGHT = "#59C7FF"
        GOLD = "#FFD77A"
        DARK_BLUE = "#10263E"

        # ニューラルネットワークの各層
        layer_sizes = [4, 5, 5, 3]

        layers = []
        connection_groups = []

        # =====================================
        # 2. ニューロンの作成
        # =====================================

        for i, count in enumerate(layer_sizes):

            layer = VGroup()

            for j in range(count):

                # ニューロンの座標
                x = (i - 1.5) * 2.5
                y = (j - (count - 1) / 2) * 0.8

                # 外側の淡い光
                glow = Circle(
                    radius=0.24,
                    stroke_width=0,
                    fill_color=BLUE_LIGHT,
                    fill_opacity=0.10
                )

                # ニューロン本体
                core = Circle(
                    radius=0.12,
                    stroke_color=BLUE_LIGHT,
                    stroke_width=2,
                    fill_color=DARK_BLUE,
                    fill_opacity=1
                )

                neuron = VGroup(glow, core)
                neuron.move_to([x, y, 0])

                layer.add(neuron)

            layers.append(layer)

        # =====================================
        # 3. 接続線を作成
        # =====================================

        for i in range(len(layers) - 1):

            group = VGroup()

            for start in layers[i]:
                for end in layers[i + 1]:

                    line = Line(
                        start.get_center(),
                        end.get_center(),
                        stroke_color="#416A91",
                        stroke_width=1,
                        stroke_opacity=0.25
                    )

                    group.add(line)

            connection_groups.append(group)

        # =====================================
        # 4. ネットワークを登場させる
        # =====================================

        all_connections = VGroup(
            *connection_groups
        )

        all_neurons = VGroup(*layers)

        network = VGroup(
            all_connections,
            all_neurons
        )

        # 最初は少し引いた画角
        self.camera.frame.scale(1.15)

        self.play(
            FadeIn(all_connections),
            run_time=1.2
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(layer, scale=0.6)
                    for layer in layers
                ],
                lag_ratio=0.25
            ),
            run_time=1.5
        )

        # カメラをゆっくり近づける
        self.play(
            self.camera.frame.animate.scale(0.9),
            run_time=2,
            rate_func=smooth
        )

        # =====================================
        # 5. 光る粒子の作成関数
        # =====================================

        def make_signal():

            # 光を半透明の円で表現
            outer = Dot(
                radius=0.16,
                color=BLUE_LIGHT,
                fill_opacity=0.12
            )

            middle = Dot(
                radius=0.09,
                color=BLUE_LIGHT,
                fill_opacity=0.4
            )

            core = Dot(
                radius=0.035,
                color=WHITE
            )

            return VGroup(outer, middle, core)

        # =====================================
        # 6. 信号の伝播アニメーション
        # =====================================

        for i, connections in enumerate(
            connection_groups
        ):

            # 0から1まで変化する進行度
            progress = ValueTracker(0)

            signals = VGroup()

            # 各接続線に粒子を配置
            for line in connections:

                signal = make_signal()

                # 各フレームで粒子位置を再計算
                def update_signal(
                    mob,
                    path=line,
                    tracker=progress
                ):
                    t = tracker.get_value()

                    # 線形補間による位置計算
                    position = interpolate(
                        path.get_start(),
                        path.get_end(),
                        t
                    )

                    mob.move_to(position)

                signal.add_updater(update_signal)

                # 初期位置を設定
                update_signal(signal)

                signals.add(signal)

            # 光の残像を作成
            trails = VGroup()

            for line in connections:

                # 残光は粒子の後ろに伸びる短い線
                trail = always_redraw(
                    lambda path=line, tracker=progress:
                    Line(
                        path.point_from_proportion(
                            max(0, tracker.get_value() - 0.16)
                        ),
                        path.point_from_proportion(
                            tracker.get_value()
                        ),
                        stroke_color=BLUE_LIGHT,
                        stroke_width=2.5,
                        stroke_opacity=0.65
                    )
                )

                trails.add(trail)

            # 残光を粒子の背後に表示
            self.add(trails)
            self.add(signals)

            # 接続線を明るくする
            self.play(
                connections.animate.set_stroke(
                    color=BLUE_LIGHT,
                    opacity=0.45
                ),
                run_time=0.2
            )

            # 0から1へ進行度を変化
            self.play(
                progress.animate.set_value(1),
                run_time=1.6,
                rate_func=linear
            )

            # 到着したニューロンを発光
            target_layer = layers[i + 1]

            self.play(
                *[
                    neuron[1].animate.set_fill(
                        GOLD,
                        opacity=1
                    )
                    for neuron in target_layer
                ],
                run_time=0.25
            )

            # Updaterを解除してから削除
            for signal in signals:
                signal.clear_updaters()

            self.remove(signals, trails)

            # 次の信号に備えて元の色に戻す
            self.play(
                *[
                    neuron[1].animate.set_fill(
                        DARK_BLUE,
                        opacity=1
                    )
                    for neuron in target_layer
                ],
                connections.animate.set_stroke(
                    color="#416A91",
                    opacity=0.25
                ),
                run_time=0.3
            )

        # =====================================
        # 7. 最後のカメラ演出
        # =====================================

        self.play(
            self.camera.frame.animate.scale(1.12),
            run_time=1.5
        )

        title = Text(
            "NEURAL SIGNAL FLOW",
            font_size=28,
            color=WHITE
        ).next_to(network, DOWN, buff=0.6)

        self.play(
            FadeIn(title, shift=UP * 0.2),
            run_time=1
        )

        self.wait(1.5)

        self.play(
            FadeOut(network),
            FadeOut(title),
            run_time=1.2
        )

