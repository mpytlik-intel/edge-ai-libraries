# ② C++ elements

Intel® DL Streamer C++ interface allows for developing new functional blocks
(source, transform and sink elements) with minimal effort. The interface
does not use any GStreamer types, so elements/blocks written in this
interface can be used in both GStreamer-based and non-GStreamer
applications.

The C++ element implementations typically inherit one of base classes,
which partially implement some functions in the corresponding abstract
interfaces:

- [BaseSource](./api_ref/class_dlstreamer_BaseSource.html) partially implements
  [Source](./api_ref/class_dlstreamer_Source.html)
- [BaseTransform](./api_ref/class_dlstreamer_BaseTransform.html) partially implements
  [Transform](./api_ref/class_dlstreamer_Transform.html)
- [BaseTransformInplace](./api_ref/class_dlstreamer_BaseTransformInplace.html) partially implements
  [Transform](./api_ref/class_dlstreamer_Transform.html)
- [BaseSink](./api_ref/class_dlstreamer_BaseSink.html) partially implements
  [Sink](./api_ref/class_dlstreamer_Sink.html) so that C++ element implements only the remaining virtual functions (mostly `read`, `process` and `write` functions) as shown in the diagram below.

⠀
**C++ interfaces and base classes**

![c++-interfaces-and-base-classes](../_images/c++-interfaces-and-base-classes.svg)

Many examples how to create C++ elements can be found on github
repository in the [src](https://github.com/open-edge-platform/edge-ai-libraries/tree/main/libraries/dl-streamer/src) folder and its sub-folders.

## Element description

The
`struct_dlstreamer_ElementDesc` structure is used to describe the input/output
capabilities and supported parameters of an element, as well provide instance
creation function. The most important fields are:

- `name` - Name of the element. Same name is used for both GStreamer and
  direct programming applications.
- `params` - Array of parameters supported by the element. In case of
  GStreamer, those will be translated to GStreamer properties.
- `input_info` - Types of input [Frames]{.title-ref} that the element
  can consume. In case of GStreamer interop, it will be represented as
  sink capabilities.
- `output_info` - Types of output [Frames]{.title-ref} that the element
  can produce. In case of GStreamer interop, it will be represented as
  source (src) capabilities.
- `create` - Pointer to a function that creates an instance of an
  element.

Here's an example of
`struct_dlstreamer_ElementDesc` structure for simple post-processing element:

```cpp
// Element parameters
ParamDescVector params_desc = {
  {"method", "Method used to post-process tensor data", "max", {"max", "softmax", "compound", "index"}},
  {"labels_file", "Path to .txt file containing object classes (one per line)", std::string()},
  {"layer_name", "Name of output layer to process (in case of multiple output tensors)", std::string()},
  {"threshold", "Threshold for confidence values", dflt::threshold, 0.0, 1.0},
};

// Element description
ElementDesc tensor_postproc_label = {
  .name = "tensor_postproc_label",
  .description = "Post-processing of classification inference to extract object classes",
  .author = "Intel Corporation",
  .params = &params_desc,
  .input_info = {MediaType::Tensors},
  .output_info = {MediaType::Tensors},
  .create = create_element<PostProcLabel>,
  .flags = 0};
```

## How to create an instance of a C++ element

Instance of C++ element can be created using the functions `create_source`,
`create_transform`, `create_sink`. These functions take pointer to
`ElementDesc`, initialization parameters (as `std::map`) and optional
context pointer as
[parameters](./api_ref/namespace_dlstreamer.md)

```cpp
auto ffmpeg_source = create_source(ffmpeg_multi_source, {{"inputs", inputs}}, ffmpeg_ctx);
```

For examples, see direct programming samples
[ffmpeg_openvino](https://github.com/open-edge-platform/edge-ai-libraries/tree/main/libraries/dl-streamer/samples/ffmpeg_openvino)
and
[ffmpeg_dpcpp](https://github.com/open-edge-platform/edge-ai-libraries/tree/main/libraries/dl-streamer/samples/ffmpeg_dpcpp).