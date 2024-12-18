from manim import *

class MergeIntervals(MovingCameraScene):
    def construct(self):
        # Set up the scene
        self.camera.frame.scale(1.2)

        # Input intervals
        intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]

        # Title
        title = Text("Merging Overlapping Intervals", font_size=36, color=GOLD)
        title.to_edge(UP)
        self.play(Write(title))

        # Create a coordinate system to better visualize intervals
        ax = Axes(
            x_range=[0, 20, 1],
            y_range=[0, 2, 1],
            x_length=10,
            y_length=2,
            axis_config={"color": WHITE}
        )
        ax.next_to(title, DOWN, buff=0.5)
        self.play(Create(ax))

        # Step 1: Sort the intervals by start time
        intervals.sort(key=lambda x: x[0])
        
        # Create interval visualization
        interval_group = VGroup()
        label_group = VGroup()

        # Generate rectangles for each interval
        for i, interval in enumerate(intervals):
            # Create rectangle
            rect = Rectangle(
                width=(interval[1] - interval[0]) * ax.x_length / 20, 
                height=0.6, 
                color=BLUE, 
                fill_opacity=0.5
            )
            
            # Position rectangle
            rect.move_to(ax.coords_to_point((interval[0] + interval[1]) / 2, 1))
            
            # Create label
            label = Text(f"[{interval[0]}, {interval[1]}]", font_size=24)
            label.next_to(rect, DOWN)
            
            interval_group.add(rect)
            label_group.add(label)

        # Display initial intervals
        self.play(
            Create(interval_group),
            Write(label_group)
        )
        self.wait(1)

        # Merging intervals process
        merged = []
        merged_group = VGroup()

        # Detailed merging animation
        for i in range(len(intervals)):
            current_start, current_end = intervals[i]
            
            # Highlight current interval
            current_highlight = SurroundingRectangle(
                VGroup(interval_group[i], label_group[i]), 
                color=YELLOW, 
                buff=0.1
            )
            self.play(Create(current_highlight))
            
            # Check if the current interval can be merged
            can_merge = False
            for j in range(len(merged)):
                previous_start, previous_end = merged[j]
                
                # Overlap condition
                if current_start <= previous_end:
                    can_merge = True
                    
                    # Merge highlight
                    merge_highlight = SurroundingRectangle(
                        VGroup(
                            merged_group[j], 
                            interval_group[i]
                        ), 
                        color=GREEN, 
                        buff=0.1
                    )
                    self.play(
                        Create(merge_highlight),
                        current_highlight.animate.set_color(GREEN)
                    )
                    
                    # Update last merged interval
                    new_interval = [min(previous_start, current_start), max(previous_end, current_end)]
                    merged[j] = new_interval
                    
                    # Update merged group
                    merged_rect = Rectangle(
                        width=(new_interval[1] - new_interval[0]) * ax.x_length / 20, 
                        height=0.6, 
                        color=GREEN, 
                        fill_opacity=0.7
                    )
                    merged_rect.move_to(ax.coords_to_point((new_interval[0] + new_interval[1]) / 2, 1))
                    
                    # Animate merging
                    self.play(
                        FadeOut(interval_group[i]),
                        FadeOut(merged_group[j]),
                        FadeOut(merge_highlight),
                        FadeOut(current_highlight)
                    )
                    
                    # Update merged group
                    merged_group[j] = merged_rect
                    
                    break
            
            # If the current interval can't be merged, add it as a new interval
            if not can_merge:
                merged.append([current_start, current_end])
                
                # Create merged rectangle
                merged_rect = Rectangle(
                    width=(current_end - current_start) * ax.x_length / 20, 
                    height=0.6, 
                    color=GREEN, 
                    fill_opacity=0.7
                )
                merged_rect.move_to(ax.coords_to_point((current_start + current_end) / 2, 1))
                
                # Animate adding new interval
                self.play(
                    FadeOut(current_highlight)
                )
                
                merged_group.add(merged_rect)

        # Final result
        result_text = Text("Merged Intervals", font_size=32, color=GOLD)
        result_text.next_to(ax, DOWN, buff=0.5)
        
        # Highlight final merged intervals
        self.play(
            FadeOut(interval_group),
            FadeOut(label_group),
            Write(result_text)
        )
        
        # Show merged intervals
        self.play(Create(merged_group))
        
        self.wait(2)