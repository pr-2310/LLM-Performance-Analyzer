import argparse
from model_analyzer import ModelAnalyzer

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("model_id", type=str, help="model id")
    parser.add_argument(
        "hardware",
        type=str,
        help="name of hardware, for example nvidia_V100 or nvidia_A6000",
    )
    parser.add_argument(
        "--source",
        type=str,
        default="huggingface",
        help="source of model, if not huggingface, will use local model in model_params.<source>",
    )
    parser.add_argument("--config_file", type=str, default=None, help="config file")
    parser.add_argument("--batchsize", type=int, default=1, help="batch size")
    parser.add_argument("--seqlen", type=int, default=1024, help="sequence length")
    parser.add_argument("--w_bit", type=int, default=16, help="weight bitwidth")
    parser.add_argument(
        "--a_bit", type=int, default=16, help="temporary activation bitwidth"
    )
    parser.add_argument("--kv_bit", type=int, default=16, help="kv cache bitwidth")
    parser.add_argument(
        "--use_flashattention", action="store_true", help="use flash attention"
    )
    return parser.parse_args()

def analyze_model(args):
    analyzer = ModelAnalyzer(
        args.model_id, args.hardware, args.config_file, source=args.source
    )
    results = analyzer.analyze(
        batchsize=args.batchsize,
        seqlen=args.seqlen,
        w_bit=args.w_bit,
        a_bit=args.a_bit,
        kv_bit=args.kv_bit,
        use_flashattention=args.use_flashattention,
    )
    analyzer.save_csv()
    return results

if __name__ == "__main__":
    args = parse_arguments()
    analyze_model(args)