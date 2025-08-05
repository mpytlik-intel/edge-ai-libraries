import importlib
from pathlib import Path
from typing import Dict, List, Tuple

import yaml


class GstPipeline:
    def __init__(self):
        pass

    def pipeline(self) -> str:
        if not hasattr(self, "_pipeline"):
            raise ValueError("Pipeline is not defined")

        return self._pipeline

    def evaluate(
        self,
        constants: dict,
        parameters: dict,
        regular_channels: int,
        inference_channels: int,
        elements: list,
    ) -> str:
        raise NotImplementedError(
            "The evaluate method must be implemented by subclasses"
        )

    def diagram(self) -> Path:
        if not hasattr(self, "_diagram"):
            raise ValueError("Diagram is not defined")

        return self._diagram

    def bounding_boxes(self) -> List:
        if not hasattr(self, "_bounding_boxes"):
            raise ValueError("Bounding Boxes is not defined")

        return self._bounding_boxes


class PipelineLoader:
    @staticmethod
    def list(pipeline_path: str = "pipelines") -> List[str]:
        """Return available pipeline folder names (not display names)."""
        pipelines_dir = Path(pipeline_path)
        return [
            name.name
            for name in pipelines_dir.iterdir()
            if name.is_dir() and not name.name.startswith("_")
        ]

    @staticmethod
    def config(pipeline_name: str, pipeline_path: str = "pipelines") -> dict:
        """Return full config dict for a pipeline."""
        config_path = Path(pipeline_path) / pipeline_name / "config.yaml"
        # Validate that config_path is within the intended pipelines directory
        pipelines_dir = Path(pipeline_path).resolve(strict=True)
        try:
            config_path_resolved = config_path.resolve(strict=True)
        except Exception:
            raise FileNotFoundError(f"{config_path} could not be resolved")
        try:
            config_path_resolved.relative_to(pipelines_dir)
        except ValueError:
            raise ValueError("Invalid pipeline name or path traversal detected")
        # At this point, config_path_resolved is guaranteed to exist and be within pipelines_dir
        return yaml.safe_load(config_path_resolved.read_text())

    @staticmethod
    def load(pipeline_name: str, pipeline_path: str = "pipelines") ->  Tuple[GstPipeline, Dict]:
        """Load pipeline class and config, or just metadata.name"""
        config = PipelineLoader.config(pipeline_name, pipeline_path)
        classname = config.get("metadata", {}).get("classname")
        if not classname:
            raise ValueError(
                f"Pipeline {pipeline_name} does not have a classname defined in config.yaml"
            )

        # NOTE: This code always imports from the pipelines directory.
        module = importlib.import_module(f"pipelines.{pipeline_name}.pipeline")
        pipeline_cls = getattr(module, classname)
        return pipeline_cls(), config
