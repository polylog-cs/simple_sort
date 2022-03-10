from solarized import *
from manim import *

text_color = GRAY
circum_color = RED
title_smaller_font_size = 60


class Intro(Scene):
    def construct(self):

        buffer = 0.5

        rozhon = Tex(
            r"\textbf{Václav Rozhoň}: script, animation", 
            color=text_color,
            font_size = 40,
        ).shift(
            DOWN * buffer
        )
        volhejn = Tex(
            r"\textbf{Václav Volhejn}: voice, script, animation",
            color=text_color,
            font_size = 40,
        ).shift(2 * DOWN * buffer)


        names = Group(rozhon, volhejn)
        names.shift(2 * DOWN + 3*LEFT)

        volhejn.align_to(names, LEFT)
        rozhon.align_to(names, LEFT)

        channel_name = Tex(r"polylog", color=text_color)
        channel_name.scale(4).shift(1 * UP + 1* LEFT)

        arxiv_img = ImageMobject("img/stanley_fung-1.png").scale_to_fit_height(
            6
        ).move_to(
            5*RIGHT + 0.5*DOWN
        )

        stanley1 = Tex("Based on this very nice paper", font_size = 50, color = text_color)
        stanley2 = Tex("by Stanley Fung", font_size = 50, color = text_color)
        stanley = Group(stanley1, stanley2).arrange(DOWN, aligned_edge = RIGHT).shift(3*DOWN+LEFT)
        # for s in [stanley1, stanley2]:
        #     s.next_to(arxiv_img, LEFT)

        run_time = Write(channel_name).run_time
        self.play(
            Write(volhejn, run_time=run_time),
            Write(rozhon, run_time=run_time),
            Write(channel_name, run_time=run_time),
        )

        self.wait()

        self.play(
            AnimationGroup(
                AnimationGroup(
                    Unwrite(volhejn, reverse=True),
                    Unwrite(rozhon),
                ),
                AnimationGroup(
                    Write(stanley1),
                    FadeIn(arxiv_img),
                ),
                AnimationGroup(
                    Write(stanley2),
                ),
                lag_ratio = 0.5
            )
            #run_time=1,
        )
        self.wait(1)


        self.play(
            Unwrite(channel_name),
            FadeOut(arxiv_img),
            FadeOut(stanley1),
            FadeOut(stanley2),
            run_time=1,
        )
        self.wait(1)

class SortAnims:
    indent = 0.5*RIGHT
    pos_cols = 3*RIGHT + 1 * DOWN
    pos_text = 6.5*LEFT + 0.5*UP
    arrow_padding = 1*DOWN
    same_pos_diff = 0.3*RIGHT
    title_font_size = 70
    title_pos = 3*UP
    colors = [RED, ORANGE, YELLOW, GREEN, TEAL, BLUE, PURPLE]

    def __init__(self, heights):
        assert len(self.colors) >= len(heights)
        # colors are by the final sorted order
        ordered_heights = sorted(heights)
        ordered_colors = []
        for i in range(len(heights)):
            ordered_colors.append(self.colors[ordered_heights.index(heights[i])])

        self.rectangles = []
        for i,(h,col) in enumerate(zip(heights, ordered_colors)):
            rec = Rectangle(width = 0.5, height = 0.4 * h, color = col, fill_color = col).set_fill(col, opacity = 1.0)
            self.rectangles.append((rec, h, None))
        
        self.rectangle_group = Group(*[obj for obj, _, _ in self.rectangles]).arrange(
            RIGHT
        ).move_to(
            self.pos_cols
        )
        for obj in self.rectangle_group:
            obj.shift((obj.get_bottom() - self.pos_cols[1]) * DOWN)

        self.delta = self.rectangles[1][0].get_bottom() - self.rectangles[0][0].get_bottom()
        self.n = len(self.rectangles) 

    def setup(self):
        setup_anims = [
            AnimationGroup(
                *[FadeIn(rec) for rec, _, _ in self.rectangles],
                AnimationGroup(
                    *[Write(txt) for txt in self.text],
                    lag_ratio=0.3
                ),
                Write(self.title),
            ),
        ]

        for i in range(len(self.rectangles)):
            rec, h, _ = self.rectangles[i]
            self.rectangles[i] = (rec, h, rec.get_center())

        return setup_anims

    def reset_columns(self):
        for rect in self.rectangles:
            (rec, _, pos) = rect
            rec.move_to(pos)

        anims = []
        for rec, _, pos in self.rectangles:
            anims.append(rec.animate.move_to(pos))
        self.rectangles.sort(key = lambda tup : tup[2][0])

        return [AnimationGroup(*anims)]

    def swap(self, i, j):
        assert i != j

        (objl, _, _) = self.rectangles[i]
        (objr, _, _) = self.rectangles[j]

        diff = (objr.get_center() - objl.get_center())[0]*RIGHT

        startl = objl.get_center()
        endl = startl + diff
        startr = objr.get_center()
        endr = startr - diff
         
        pathl = Arc(radius = (endl-startl)[0]/2.0, start_angle = -PI, angle = PI, arc_center = (startl+endl)/2)
        pathr = Arc(radius = (endl-startl)[0]/2.0, start_angle = 0, angle = PI, arc_center = (startr+endr)/2)
        #Line(startr, endr)

        anim = AnimationGroup(
            MoveAlongPath(objl, pathl),
            MoveAlongPath(objr, pathr)
        )

        #the animation is not done yet, so we need to move them manually and rememeber the old position as the third param of the tuple
        objl.shift(diff)
        objr.shift(-diff)        

        self.rectangles[i], self.rectangles[j] = self.rectangles[j], self.rectangles[i]

        return anim

    def initarrows(self, i, j, name_i = "i", name_j = "j"):
        # create the objects
        self.arrow_i = Arrow(start = 0*UP, end = 0.5*UP, buff = 0, color = RED)
        self.txt_i = MathTex(name_i, color = text_color)
        self.arrow_group_i = Group(self.arrow_i, self.txt_i).arrange(
            DOWN
        ).move_to(
            self.rectangles[i][0].get_bottom() + self.arrow_padding
        )
        
        self.arrow_j = Arrow(start = 0*UP, end = 0.5*UP, buff = 0, color = RED)
        self.txt_j = MathTex(name_j, color = text_color)
        self.arrow_group_j = Group(self.arrow_j, self.txt_j).arrange(
            DOWN
        ).move_to(
            self.rectangles[j][0].get_bottom() + self.arrow_padding
        )

        self.diff_i_j = (-self.arrow_group_j.get_top() + self.arrow_group_i.get_top())[1] * UP
        self.arrow_group_j.shift(self.diff_i_j)

        # same position change
        if i == j:
            self.arrow_group_i.shift(-self.same_pos_diff/2)
            self.arrow_group_j.shift(self.same_pos_diff/2)


        # return anims
        anims = [
            AnimationGroup(
                Create(self.arrow_i),
                Write(self.txt_i),
                Create(self.arrow_j),
                Write(self.txt_j),
            )
        ]

        self.start_pos_i = self.arrow_group_i.get_center()
        self.start_pos_j = self.arrow_group_j.get_center()

        return anims        

    def changearrows(self, i, j):

        new_pos_i = self.rectangles[i][0].get_bottom() + self.arrow_padding
        new_pos_j = self.rectangles[j][0].get_bottom() + self.arrow_padding + self.diff_i_j

        if i == j:
            new_pos_i += -self.same_pos_diff/2
            new_pos_j += self.same_pos_diff/2


        anims = [
            AnimationGroup(
                self.arrow_group_i.animate.move_to(
                   new_pos_i 
                ),
                self.arrow_group_j.animate.move_to(
                    new_pos_j
                ),
            )
        ]

        self.arrow_group_i.move_to(
            new_pos_i
        )
        self.arrow_group_j.move_to(
            new_pos_j
        )

        return anims

    def removearrows(self):
        self.arrow_group_i.move_to(self.start_pos_i)
        self.arrow_group_j.move_to(self.start_pos_j)

        anims = [
            AnimationGroup(
                Uncreate(self.arrow_i),
                Uncreate(self.arrow_j),
                Unwrite(self.txt_i),
                Unwrite(self.txt_j),
            )
        ]

        return anims

    def run_bubblesort(self):      
        # bubble sort pseudocode
        lines = [
            "{{for i = 1 to }}{{n-1}}{{:}}",
            "{{for j =}}{{1}}{{ to n-1:}}",
            "{{if a[j+1] }}{{< }}{{ a[j]:}}",
            "{{swap(a[j], a[j+1])}}"
        ]

        self.title = Tex("Bubblesort", color = text_color, font_size = self.title_font_size).move_to(
            self.title_pos
        )

        self.text = [
            Tex(str, color = text_color)
            for str in lines
        ]

        text_group = Group(*self.text).arrange(DOWN)
        
        for i in range(4):
            self.text[i].align_to(Dot(self.pos_text + i * self.indent), LEFT)

  
        anims = [
            *self.setup(),
        ]

        anims += self.initarrows(0, 1, name_i = "j", name_j = r"j\!+\!1")

        # run the algorithm
        for i in range(self.n-1):
            for j in range(self.n-1):
                anims += self.changearrows(j, j+1)
                (_, hl, _) = self.rectangles[j]
                (_, hr, _) = self.rectangles[j+1]

                #swap the columns
                if hl > hr:
                    anims.append(
                        self.swap(j, j+1)
                    )

        anims += self.removearrows()



        # final cleanup
        anims.append(
            AnimationGroup(
                *[Unwrite(txt) for txt in self.text],
            )
        )

        # move columns back to their original position
        anims += self.reset_columns()

        return anims

    def run_selectsort(self, weird_sort = False, sign = '<', title = "Selectsort", last = False):      
        # select sort pseudocode
        lines = [
            "{{for i = 1 to }}{{n}}{{:}}",
            "{{for j = }}" + ("{{i+1}}" if not weird_sort else "{{1}}") + "{{ to }}{{n:}}",
            "{{if a[i] }}{{" + sign + "}}{{ a[j]:}}",
            "swap(a[i], a[j])"
        ]
        anims = []

        selecttext = [
            Tex(str, color = text_color)
            for str in lines
        ]

        for i in range(4):
            selecttext[i].align_to(self.text[i], LEFT).align_to(self.text[i], UP)

        # new title
        newtitle = Tex(title, color = text_color, font_size = self.title_font_size).move_to(self.title.get_center())

        # change previous pseudocode/title to this one
        anims += [[
            AnimationGroup(
                *[ReplacementTransform(orig, new) for orig, new in zip(self.text, selecttext)],
                ReplacementTransform(self.title, newtitle)
            ), 
            Wait()
        ]]
        self.text = selecttext
        self.title = newtitle

        if weird_sort == True:
            anims[0] += self.initarrows(0, 0)
        else:
            anims[0] += self.initarrows(0, 1)

        # run the algorithm
        for i in range(self.n):
            anims_forloop = []
            rng = range(i+1, self.n)
            if weird_sort == True:
                rng = range(self.n)

            for j in rng:
                anims_forloop += self.changearrows(i, j)
                (_, hl, _) = self.rectangles[i]
                (_, hr, _) = self.rectangles[j]

                #swap the columns
                if (sign == '<' and hl < hr) or (sign == '>' and hl > hr) :
                    anims_forloop.append(
                        self.swap(i, j)
                    )
                else:
                    anims_forloop.append(
                        Wait(0.01)
                    )

            anims.append(anims_forloop)

        anims += [self.removearrows()]

        # move columns back to their original position
        if last == False:
            anims[-1] += self.reset_columns()
        else:
            self.reset_columns()
            anims[-1].append(
                AnimationGroup(
                    *[FadeOut(rec[0]) for rec in self.rectangles]
                )
            )


        return anims

class Algorithms(Scene):
    def construct(self):
        skip = False

        self.next_section(name = "bubblesort", skip_animations=skip)

        permutation = [4, 6, 2, 3, 5, 1]
        permutation = [3, 7, 2, 4, 6, 5, 1]
        sort_obj = SortAnims(permutation)
    
        bubble_anims = sort_obj.run_bubblesort()

        # run bubble sort
        for anim in bubble_anims:
            self.play(anim, run_time = 1)
        self.wait()

        # run select sort
        self.next_section(name = "selectsort", skip_animations=skip)
        select_anims = sort_obj.run_selectsort(weird_sort=False, sign='>')
        num_anim_groups = len(select_anims)

        for i, anim_group in enumerate(select_anims):
            # highlight parts of select sort code
            if i == num_anim_groups - 2:
                self.wait()
                self.play(
                    Circumscribe(sort_obj.text[0], color = circum_color),
                )
                self.play(
                    Circumscribe(sort_obj.text[1], color = circum_color),
                )
                self.wait()
                self.play(
                    AnimationGroup(
                        Circumscribe(
                            Group(
                                sort_obj.text[2],
                                sort_obj.text[3]
                            ), color = circum_color
                        )
                    )
                )
                self.wait()

            # play the chunk of the animations
            for anim in anim_group:
                self.play(anim, run_time = 1)


        self.wait()


        self.play(
            Circumscribe(
                sort_obj.text[1][1],
                color = circum_color
            )
        )
        self.wait()

        # run weird sort
        self.next_section(name = "weirdsort1", skip_animations=skip)
        weird_anims = sort_obj.run_selectsort(weird_sort=True, sign='>', title = "Simplesort?")
        num_anim_groups = len(weird_anims)

        for i, anim_group in enumerate(weird_anims):
            # play the chunk of the animations
            for j, anim in enumerate(anim_group):
                #print(i, j, len(anim_group))
                if i == 0 and j == len(anim_group)-1:
                    self.play(
                        Flash(
                            Group(*sort_obj.text),
                            flash_radius=2,
                            num_lines=16,
                        )
                    )   
                    self.wait()
                    self.play(
                        Circumscribe(sort_obj.text[0] , color = circum_color)
                    )
                    self.wait()
                    self.play(
                        Circumscribe(sort_obj.text[1], color = circum_color)
                    )
                    self.wait()
                    self.play(
                        Circumscribe(Group(sort_obj.text[2], sort_obj.text[3]), color = circum_color)
                    )
                    self.wait()

                self.play(anim, run_time = 1)


        self.wait()

        # run weird sort for the second time
        self.next_section(name = "weirdsort2", skip_animations=False)
        weird_anims = sort_obj.run_selectsort(weird_sort=True, sign='>', title = "Simplesort?", last = True)
        num_anim_groups = len(weird_anims)

        for i, anim_group in enumerate(weird_anims):

            # play the chunk of the animations
            for j, anim in enumerate(anim_group):
                if i == 5 and j == 1: # highlight the smallest elem at the beginning of the explain iteration
                    rectangles_sorted = sorted(sort_obj.rectangles, key = lambda x : x[0].get_center()[0])
                    self.play(Circumscribe(rectangles_sorted[3][0]), color = circum_color)
                    self.wait()
                    self.play(Circumscribe(rectangles_sorted[4][0]), color = circum_color)
                    self.wait()

                if i>1 and j == 2*i-1:
                    new_brace = Brace(
                        Group(*[r[0] for r in rectangles_sorted[0:i]]), 
                        DOWN,
                        color = text_color,
                    ).shift(1.5*DOWN)
                    self.play(
                        brace.animate.become(new_brace),
                        brace_txt.animate.next_to(new_brace, DOWN, buff = 0.1)
                    )
                    self.wait()

                if i == len(weird_anims)-1 and j == len(anim_group)-1:
                    anim = AnimationGroup(
                        anim,
                        FadeOut(brace),
                        Unwrite(brace_txt)
                    )

                self.play(anim, run_time = 1)


            if i == 1:
                #highlight the smallest elem after first iteration                
                rectangles_sorted = sorted(sort_obj.rectangles, key = lambda x : x[0].get_center()[0])
                self.play(Circumscribe(rectangles_sorted[0][0]), color = circum_color)
                self.wait()

                # create brace
                brace = Brace(rectangles_sorted[0][0], DOWN, color = text_color).shift(1.5*DOWN)
                brace_txt = Tex("sorted", color = text_color).next_to(brace, DOWN, buff = 0.1)
                self.play(
                    Create(brace),
                    Write(brace_txt)
                )
                self.wait()                
            
        self.wait()

        # change to insert sort
        self.next_section(name = "outro", skip_animations=False)
        self.play(
            Circumscribe(
                sort_obj.text[1][3], color = circum_color
            )
        )
        self.wait()
        newline = Tex(
            "{{for j = }}{{1}}{{ to }}{{i:}}",
            color = text_color
        ).move_to(
            sort_obj.text[1].get_center()
        ).align_to(
            sort_obj.text[1], 
            LEFT
        )
        self.play(
            sort_obj.text[1].animate.become(newline)
        )
        self.wait()

        insert_title = Tex(
            "(reverse) Insertsort",
            font_size = title_smaller_font_size,
            color = text_color
        ).move_to(
            sort_obj.text[0].get_center()
        ).align_to(
            sort_obj.text[0], 
            LEFT
        ).shift(
            1*UP
        )
        self.play(
            sort_obj.title.animate.become(
                insert_title
            )
        )        

        # create select sort pseudocode
        
        shft = 7*RIGHT
        select_title = Tex(
            "Selectsort",
            font_size = title_smaller_font_size,
            color = text_color
        ).move_to(
            sort_obj.title.get_center()
        ).align_to(
            sort_obj.title,
            LEFT
        ).shift(
            shft
        )

        select_lines = [
            "{{for i = 1 to }}{{n}}{{:}}",
            "{{for j = }}" + "{{i+1}}" + "{{ to }}{{n:}}",
            "{{if a[i] }}{{>}}{{ a[j]:}}",
            "swap(a[i], a[j])"
        ] 
        select_text = [
            Tex(str, color = text_color)
            for str in select_lines
        ]
        for i, text in enumerate(select_text):
            text.move_to(
                sort_obj.text[i].get_center()
            ).align_to(
                sort_obj.text[i],
                LEFT
            ).shift(
                shft
            )

        self.play(
            Write(select_title),
            *[Write(txt) for txt in select_text]
        )

        self.wait()

        self.play(
            Circumscribe(sort_obj.text[1], color = circum_color)
        )
        self.play(
            Circumscribe(select_text[1], color = circum_color)
        )
        self.wait()


        # final join of the two codes
        simple_lines = [
            "{{for i = 1 to }}{{n}}{{:}}",
            "{{for j = }}" + "{{1}}" + "{{ to }}{{n:}}",
            "{{if a[i] }}{{>}}{{ a[j]:}}",
            "swap(a[i], a[j])"
        ]
        simple_text = [
            Tex(str, color = text_color, font_size = 80)
            for str in simple_lines
        ]
        Group(*simple_text).arrange(DOWN).shift(LEFT)
        for i in range(4):
            simple_text[i].align_to(Dot(simple_text[0].get_left() + i * sort_obj.indent*1.5), LEFT)

        simple_text2 = simple_text.copy()

        self.play(
            *[txt.animate.become(new_txt) for txt, new_txt in zip(sort_obj.text, simple_text)],
            *[txt.animate.become(new_txt) for txt, new_txt in zip(select_text, simple_text2)],
            FadeOut(sort_obj.title),
            FadeOut(select_title)
        )        
        self.wait()

