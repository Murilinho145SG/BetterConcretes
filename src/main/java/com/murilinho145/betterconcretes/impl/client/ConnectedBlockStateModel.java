package com.murilinho145.betterconcretes.impl.client;

import com.mojang.math.Quadrant;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import com.murilinho145.betterconcretes.BetterConcretes;
import com.murilinho145.betterconcretes.impl.blocks.ConnectedConcreteBlock;
import net.minecraft.client.renderer.block.BlockAndTintGetter;
import net.minecraft.client.renderer.block.dispatch.BlockStateModel;
import net.minecraft.client.renderer.block.dispatch.BlockStateModelPart;
import net.minecraft.client.renderer.chunk.ChunkSectionLayer;
import net.minecraft.client.resources.model.ModelBaker;
import net.minecraft.client.resources.model.ModelDebugName;
import net.minecraft.client.resources.model.ResolvableModel;
import net.minecraft.client.resources.model.geometry.BakedQuad;
import net.minecraft.client.resources.model.sprite.Material;
import net.minecraft.client.resources.model.sprite.MaterialBaker;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.resources.Identifier;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.client.model.DynamicBlockStateModel;
import net.neoforged.neoforge.client.model.block.CustomUnbakedBlockStateModel;
import net.neoforged.neoforge.client.model.quad.MutableQuad;
import net.neoforged.neoforge.client.model.quad.UVTransform;

import java.util.List;

public class ConnectedBlockStateModel implements DynamicBlockStateModel {

    public static final Identifier LOADER_ID = Identifier.fromNamespaceAndPath(BetterConcretes.MODID, "connected");

    // [face ordinal] -> [top, right, bottom, left] neighbor indices (0=north,1=south,2=east,3=west,4=up,5=down)
    private static final int[][] FACE_EDGE_MAP = {
            {1, 2, 0, 3}, // DOWN
            {0, 2, 1, 3}, // UP
            {4, 3, 5, 2}, // NORTH (UV mirrored: left/right swapped)
            {4, 2, 5, 3}, // SOUTH (UV mirrored)
            {4, 1, 5, 0}, // WEST
            {4, 0, 5, 1}, // EAST
    };

    // [edgeBits 0..15] -> [patternIdx 0..5, rotationDegrees]
    private static final int[][] PATTERN_LOOKUP = {
            {0, 0}, {1, 90}, {1, 0}, {2, 0}, {1, 270}, {3, 0}, {2, 270}, {4, 0},
            {1, 180}, {2, 90}, {3, 90}, {4, 90}, {2, 180}, {4, 180}, {4, 270}, {5, 0},
    };

    private final BlockStateModelPart[] parts; // 64 entries
    private final Material.Baked particleMaterial;
    private final int materialFlags;

    private ConnectedBlockStateModel(BlockStateModelPart[] parts, Material.Baked particleMaterial, int materialFlags) {
        this.parts = parts;
        this.particleMaterial = particleMaterial;
        this.materialFlags = materialFlags;
    }

    @Override
    public void collectParts(RandomSource random, List<BlockStateModelPart> output) {
        // Item form / no world — fully disconnected
        output.add(parts[0]);
    }

    @Override
    public void collectParts(BlockAndTintGetter level, BlockPos pos, BlockState state,
                             RandomSource random, List<BlockStateModelPart> output) {
        output.add(parts[stateIndex(state)]);
    }

    @Override
    public Material.Baked particleMaterial() {
        return particleMaterial;
    }

    @Override
    public int materialFlags() {
        return materialFlags;
    }

    private static int stateIndex(BlockState state) {
        int idx = 0;
        if (state.getValue(ConnectedConcreteBlock.NORTH)) idx |= 1;
        if (state.getValue(ConnectedConcreteBlock.SOUTH)) idx |= 2;
        if (state.getValue(ConnectedConcreteBlock.EAST))  idx |= 4;
        if (state.getValue(ConnectedConcreteBlock.WEST))  idx |= 8;
        if (state.getValue(ConnectedConcreteBlock.UP))    idx |= 16;
        if (state.getValue(ConnectedConcreteBlock.DOWN))  idx |= 32;
        return idx;
    }

    private static int edgeBits(int stateIdx, Direction face) {
        boolean[] connected = {
                (stateIdx & 1) != 0, (stateIdx & 2) != 0, (stateIdx & 4) != 0,
                (stateIdx & 8) != 0, (stateIdx & 16) != 0, (stateIdx & 32) != 0,
        };
        int[] edgeMap = FACE_EDGE_MAP[face.ordinal()];
        int bits = 0;
        if (!connected[edgeMap[0]]) bits |= 8; // top
        if (!connected[edgeMap[1]]) bits |= 4; // right
        if (!connected[edgeMap[2]]) bits |= 2; // bottom
        if (!connected[edgeMap[3]]) bits |= 1; // left
        return bits;
    }

    private static Quadrant quadrant(int rotationDeg) {
        return switch (rotationDeg) {
            case 90 -> Quadrant.R90;
            case 180 -> Quadrant.R180;
            case 270 -> Quadrant.R270;
            default -> Quadrant.R0;
        };
    }

    public record Unbaked(Identifier texturePrefix) implements CustomUnbakedBlockStateModel {
        public static final MapCodec<Unbaked> MAP_CODEC = RecordCodecBuilder.mapCodec(inst -> inst.group(
                Identifier.CODEC.fieldOf("texture_prefix").forGetter(Unbaked::texturePrefix)
        ).apply(inst, Unbaked::new));

        @Override
        public MapCodec<Unbaked> codec() {
            return MAP_CODEC;
        }

        @Override
        public BlockStateModel bake(ModelBaker baker) {
            ModelDebugName debugName = () -> "betterconcretes:connected[" + texturePrefix + "]";
            MaterialBaker materials = baker.materials();
            Material.Baked[] sprites = new Material.Baked[6];
            for (int i = 0; i < 6; i++) {
                Identifier spriteId = Identifier.fromNamespaceAndPath(
                        texturePrefix.getNamespace(),
                        texturePrefix.getPath() + "_ctm_" + i
                );
                sprites[i] = materials.get(new Material(spriteId), debugName);
            }
            Material.Baked particle = sprites[5];

            BakedQuad[][] quads = new BakedQuad[64][6];
            MutableQuad mutable = new MutableQuad();
            for (int stateIdx = 0; stateIdx < 64; stateIdx++) {
                for (Direction dir : Direction.values()) {
                    int edgeBits = edgeBits(stateIdx, dir);
                    int patternIdx = PATTERN_LOOKUP[edgeBits][0];
                    int rotation = PATTERN_LOOKUP[edgeBits][1];

                    mutable.reset();
                    mutable.setFullCubeFace(dir);
                    mutable.setSprite(sprites[patternIdx]);
                    mutable.bakeUvsFromPosition(UVTransform.of(quadrant(rotation), false, false));
                    quads[stateIdx][dir.ordinal()] = mutable.toBakedQuad();
                }
            }

            BlockStateModelPart[] parts = new BlockStateModelPart[64];
            for (int i = 0; i < 64; i++) {
                parts[i] = new Part(quads[i], particle);
            }
            return new ConnectedBlockStateModel(parts, particle, 0);
        }

        @Override
        public void resolveDependencies(ResolvableModel.Resolver resolver) {
            // No model-parent deps; sprite refs don't need markDependency.
        }
    }

    private static final class Part implements BlockStateModelPart {
        private final List<List<BakedQuad>> perDirection;
        private final List<BakedQuad> nonCulled;
        private final Material.Baked particle;

        Part(BakedQuad[] faces, Material.Baked particle) {
            this.particle = particle;
            this.perDirection = List.of(
                    List.of(faces[0]), List.of(faces[1]), List.of(faces[2]),
                    List.of(faces[3]), List.of(faces[4]), List.of(faces[5])
            );
            this.nonCulled = List.of();
        }

        @Override
        public List<BakedQuad> getQuads(Direction direction) {
            if (direction == null) return nonCulled;
            return perDirection.get(direction.ordinal());
        }

        @Override
        public boolean useAmbientOcclusion() {
            return true;
        }

        @Override
        public Material.Baked particleMaterial() {
            return particle;
        }

        @Override
        public int materialFlags() {
            return 0;
        }
    }
}
