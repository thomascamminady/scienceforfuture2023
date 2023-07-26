import altair as alt
import pandas as pd


class PalmerPenguins:
    def __init__(self):
        self.df = pd.read_csv("https://pos.it/palmer-penguins-github-csv")
        self.names = ["Adelie", "Chinstrap", "Gentoo"]
        self.colors = ["#FF8C00", "#A020F0", "#008B8B"]
        self.scale = alt.Scale(domain=self.names, range=self.colors)

    def chart(
        self,
        df: pd.DataFrame | None = None,
        width: float = 400,
        height: float = 400,
        circle_size: float = 60,
        discard_chinstrap: bool = False,
        sample_n: int | None = None,
        color_species: bool = True,
    ) -> alt.Chart:
        """Creates a palmer penguins chart."""
        if df is None:
            df = self.df

        scale = self.scale
        if discard_chinstrap:
            df = df.loc[df["species"] != "Chinstrap"]
            scale = alt.Scale(
                domain=["Adelie", "Gentoo"],
                range=["#FF8C00", "#008B8B"],
            )
        if sample_n is not None:
            df = df.sample(sample_n, random_state=1)

        if color_species:
            color = alt.Color("species", scale=scale)
        else:
            color = alt.value("black")

        return (
            alt.Chart(df)
            .mark_circle(size=circle_size)
            .encode(
                x=alt.X("bill_length_mm", scale=alt.Scale(domain=(30, 60))),
                y=alt.Y("bill_depth_mm", scale=alt.Scale(domain=(13, 22))),
                color=color,
                tooltip=["species", "sex", "island"],
            )
            .properties(width=width, height=height)
        )

    def line(self) -> alt.Chart:
        """SVM line."""
        return (
            alt.Chart(
                pd.DataFrame({"bill_length_mm": [30, 64], "bill_depth_mm": [13, 22]})
            )
            .mark_line(color="black", strokeDash=[4, 4], clip=True)
            .encode(
                alt.X("bill_length_mm", scale=alt.Scale(domain=(30, 60))),
                alt.Y("bill_depth_mm", scale=alt.Scale(domain=(13, 22))),
            )
            .properties(width=800, height=400)
        )

    def area(self) -> alt.Chart:
        """Shade areas."""
        return (
            alt.Chart(
                pd.DataFrame(
                    {
                        "bill_length_mm": [30, 64, 30, 64],
                        "bill_depth_mm": [13, 22, 100, 100],
                        "species": ["Gentoo", "Gentoo", "Adelie", "Adelie"],
                    }
                )
            )
            .mark_area(clip=True, opacity=0.2)
            .encode(
                x=alt.X("bill_length_mm", scale=alt.Scale(domain=(30, 60))),
                y=alt.Y(
                    "bill_depth_mm", stack="zero", scale=alt.Scale(domain=(13, 22))
                ),
                color=alt.Color(
                    "species",
                    scale=alt.Scale(
                        domain=["Adelie", "Gentoo"],
                        range=["#FF8C00", "#008B8B"],
                    ),
                ),
            )
            .properties(width=800, height=400)
        )
