import argparse  # type: ignore
import json
from tqdm import tqdm
from openai_handler import generate_use_all_icl

# For rendering stage
from diagramgigen import DiagramGLIGEN
from PIL import ImageDraw, ImageFont

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    # 📌 Existing Stage 1 arguments
    parser.add_argument(
        "--test_file",
        type=str,
        default="src/my_email_workflow_prompt.txt",
        help="Path to your custom prompt JSON file"
    )
    parser.add_argument(
        "--save_file",
        type=str,
        default="generated_diagram_plan.json",
        help="Path to save the generated diagram plan"
    )

    # ➕ New arguments for Stage 2
    parser.add_argument(
        "--plan_file",
        type=str,
        default=None,
        help="(Optional) Use an existing plan JSON to skip planning"
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default=None,
        help="Where to save the final diagram image (e.g., flowchart.png)"
    )
    parser.add_argument(
        "--render",
        action="store_true",
        help="If provided, render and save the diagram image after planning"
    )

    args = parser.parse_args()
    save_file = args.save_file

    # Stage 1: Planning
    with open(args.test_file, "r") as f:
        data = json.load(f)

    out = {}
    for sample in tqdm(data, desc="Generating Diagram Plans"):
        diagram, corrections, attempts = generate_use_all_icl(
            sample["caption"], sample["topic"]
        )
        out[sample["image"]] = {
            "image": sample["image"],
            "caption": sample["caption"],
            "diagram": diagram,
            "corrections": corrections,
            "attempts": attempts,
        }
        with open(save_file, "w") as f:
            json.dump(out, f, indent=2)

    # 🖼 Stage 2: Rendering
    if args.render:
        plan_path = args.plan_file or save_file
        with open(plan_path, "r") as f:
            plan = json.load(f)

        gen = DiagramGLIGEN()
        img = gen.render(plan)

        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        for ent in plan.get("entities", []):
            if ent.get("type") == "text":
                x, y = ent["bbox"][0], ent["bbox"][1]
                draw.text((x, y), ent["content"], fill="black", font=font)

        img.save(args.output_file)
        print(f"🖼 Diagram rendered and saved to {args.output_file}")
